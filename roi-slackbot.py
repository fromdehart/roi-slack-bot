import os
import logging
from dotenv import load_dotenv
from slack_bolt import App
from slack_bolt.adapter.flask import SlackRequestHandler
from flask import Flask, request
from graph_generator import generate_roi_graph
import tempfile

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Check for required environment variables
slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
slack_signing_secret = os.environ.get("SLACK_SIGNING_SECRET")

if not slack_bot_token:
    logger.error("SLACK_BOT_TOKEN environment variable is not set")
    raise ValueError("SLACK_BOT_TOKEN environment variable is required")

if not slack_signing_secret:
    logger.error("SLACK_SIGNING_SECRET environment variable is not set")
    raise ValueError("SLACK_SIGNING_SECRET environment variable is required")

# Initialize Slack app
app = App(
    token=slack_bot_token,
    signing_secret=slack_signing_secret
)

# Initialize Flask for Heroku
flask_app = Flask(__name__)
handler = SlackRequestHandler(app)

@app.command("/roi")
def handle_roi_command(ack, respond, command):
    """Handle /roi slash command"""
    ack()
    
    user_text = command['text']
    channel_id = command['channel_id']
    user_id = command['user_id']
    
    if not user_text.strip():
        respond({
            "text": "Please provide a description for your ROI graph!\nExample: `/roi VR training vs traditional training over 3 years`",
            "response_type": "ephemeral"
        })
        return
    
    # Send immediate response
    respond({
        "text": f"🎯 Generating ROI graph for: *{user_text}*\nThis may take 15-30 seconds...",
        "response_type": "ephemeral"
    })
    
    try:
        # Generate the graph
        logger.info(f"Generating graph for user {user_id}: {user_text}")
        image_path = generate_roi_graph(user_text)
        
        # Upload image to Slack using the modern method
        result = app.client.files_upload_v2(
            channel=channel_id,
            file=image_path,
            title=f"ROI Analysis: {user_text[:50]}{'...' if len(user_text) > 50 else ''}",
            initial_comment=f"📊 Here's your ROI analysis for: *{user_text}*"
        )
        
        # Clean up temp file
        if os.path.exists(image_path):
            os.remove(image_path)
            
        logger.info(f"Successfully uploaded graph for user {user_id}")
        
    except Exception as e:
        logger.error(f"Error generating graph: {str(e)}")
        
        # Send error message
        app.client.chat_postMessage(
            channel=channel_id,
            text=f"❌ Sorry, I couldn't generate that graph. Error: {str(e)[:200]}...\n\nTry rephrasing your request or contact support."
        )

@app.command("/roi-help")
def handle_help_command(ack, respond):
    """Provide help for the ROI bot"""
    ack()
    
    help_text = """
📊 *ROI Graph Generator Help*

*Usage:* `/roi [your request]`

*Example requests:*
• `/roi VR training vs traditional training ROI over 3 years`
• `/roi Cost savings from VR implementation quarterly breakdown`
• `/roi Training efficiency improvements monthly comparison`
• `/roi Employee satisfaction before and after VR training`

*Tips:*
• Be specific about time periods (monthly, quarterly, yearly)
• Mention what you're comparing (VR vs traditional, before vs after)
• Include context about your industry if relevant

*Need help?* Contact your admin or try simpler requests first.
    """
    
    respond({
        "text": help_text,
        "response_type": "ephemeral"
    })

# Health check endpoint for Heroku
@flask_app.route("/health", methods=["GET"])
def health_check():
    return "ROI Bot is running! 🎯", 200

# Slack events endpoint
@flask_app.route("/slack/events", methods=["POST", "GET"])
def slack_events():
    if request.method == "GET":
        # Handle URL verification challenge
        challenge = request.args.get("challenge")
        if challenge:
            return challenge, 200
        return "OK", 200
    else:
        try:
            # Log request details for debugging
            logger.info(f"Received POST request with content-type: {request.content_type}")
            logger.info(f"Request headers: {dict(request.headers)}")
            request_data = request.get_data()
            logger.info(f"Request data length: {len(request_data)}")
            
            # Check if request has data
            if not request_data:
                logger.warning("Empty request body received")
                return {"error": "Empty request body"}, 400
            
            # Handle POST requests (slash commands, events)
            response = handler.handle(request)
            logger.info(f"Handler response: {response}")
            return response
            
        except Exception as e:
            logger.error(f"Error handling Slack request: {str(e)}")
            logger.error(f"Request data: {request.get_data()}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            # Return a proper response to avoid JSON parsing errors
            return {"error": str(e)}, 400

# Default route
@flask_app.route("/", methods=["GET"])
def home():
    return """
    <h1>ROI Graph Generator Bot</h1>
    <p>Status: ✅ Running</p>
    <p>Use <code>/roi [your request]</code> in Slack to generate ROI graphs.</p>
    <p>Use <code>/roi-help</code> for more information.</p>
    """, 200

if __name__ == "__main__":
    # For local development
    port = int(os.environ.get("PORT", 3000))
    flask_app.run(debug=True, host="0.0.0.0", port=port)