#!/usr/bin/env python3
import os
import logging
from dotenv import load_dotenv

print("Starting minimal test...")

# Load environment variables
load_dotenv()
print("✓ Environment loaded")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
print("✓ Logging configured")

# Test imports
try:
    from slack_bolt import App
    print("✓ slack_bolt imported")
except Exception as e:
    print(f"✗ slack_bolt import failed: {e}")

try:
    from slack_bolt.adapter.flask import SlackRequestHandler
    print("✓ SlackRequestHandler imported")
except Exception as e:
    print(f"✗ SlackRequestHandler import failed: {e}")

try:
    from flask import Flask, request
    print("✓ Flask imported")
except Exception as e:
    print(f"✗ Flask import failed: {e}")

try:
    from graph_generator import generate_roi_graph
    print("✓ graph_generator imported")
except Exception as e:
    print(f"✗ graph_generator import failed: {e}")

print("✓ All imports successful")

# Test environment variables
slack_bot_token = os.environ.get("SLACK_BOT_TOKEN")
slack_signing_secret = os.environ.get("SLACK_SIGNING_SECRET")

print(f"SLACK_BOT_TOKEN present: {bool(slack_bot_token)}")
print(f"SLACK_SIGNING_SECRET present: {bool(slack_signing_secret)}")

# Test Flask app
flask_app = Flask(__name__)
print("✓ Flask app created")

@flask_app.route("/")
def home():
    return "Minimal test app is working!", 200

if __name__ == "__main__":
    print("✓ Starting Flask app...")
    flask_app.run(debug=False, host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
