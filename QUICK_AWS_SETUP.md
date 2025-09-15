# 🚀 Quick AWS Setup (Manual Method)

## Step 1: Create AWS Account
1. Go to [aws.amazon.com](https://aws.amazon.com) 
2. Click "Create an AWS Account"
3. Choose "Personal" account
4. Add payment method (free tier won't charge you)

## Step 2: Create Deployment Package
Run this command in your project directory:

```bash
# Create a ZIP file for AWS
zip -r roi-slack-bot-aws.zip . -x@.ebignore
```

## Step 3: Deploy to Elastic Beanstalk

### Via AWS Console:
1. Go to [AWS Elastic Beanstalk](https://console.aws.amazon.com/elasticbeanstalk/)
2. Click "Create Application"
3. **Application name**: `roi-slack-bot`
4. **Platform**: Python 3.9
5. **Upload your code**: Select the `roi-slack-bot-aws.zip` file
6. Click "Create environment"

### Wait for deployment (5-10 minutes)

## Step 4: Set Environment Variables
1. In your Elastic Beanstalk dashboard
2. Go to **Configuration** → **Software** 
3. Add these environment variables:
   ```
   SLACK_BOT_TOKEN = xoxb-your-bot-token
   SLACK_SIGNING_SECRET = your-signing-secret  
   OPENAI_API_KEY = your-openai-key
   ```
4. Click "Apply"

## Step 5: Update Slack App
1. Your app URL will be: `http://roi-slack-bot-env.region.elasticbeanstalk.com`
2. Update Slack app URLs:
   - **Request URL**: `http://your-url/slack/events`
   - **Slash Command URLs**: `http://your-url/slack/events`

## Step 6: Test
1. Visit your app URL in browser
2. Try `/roi test graph` in Slack

---

**That's it!** Your bot should be running on AWS free tier! 🎉
