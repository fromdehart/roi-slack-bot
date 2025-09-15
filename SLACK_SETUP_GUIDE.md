# 🚀 Slack Bot Setup Guide

## Step 1: Create Slack App from Manifest

1. Go to: https://api.slack.com/apps
2. Click **"Create New App"**
3. Select **"From an app manifest"**
4. Choose your workspace
5. Copy the contents of `slack_app_manifest.yaml` and paste it
6. Click **"Create"**

## Step 2: Get Your Tokens

After creating the app, you'll need:

1. **Bot User OAuth Token** (starts with `xoxb-`)
   - Go to "OAuth & Permissions" 
   - Copy the "Bot User OAuth Token"

2. **Signing Secret**
   - Go to "Basic Information"
   - Copy the "Signing Secret"

## Step 3: Update Your .env File

Add these to your `.env` file:
```bash
SLACK_BOT_TOKEN=xoxb-your-actual-token-here
SLACK_SIGNING_SECRET=your-actual-signing-secret-here
```

## Step 4: Start ngrok for Local Testing

1. Install ngrok: https://ngrok.com/download
2. Start tunnel: `ngrok http 3000`
3. Copy the ngrok URL (e.g., `https://abc123.ngrok.io`)

## Step 5: Update Slack App URLs

Replace `https://your-ngrok-url.ngrok.io` in the manifest with your actual ngrok URL:

1. Go to your Slack app dashboard
2. Update these URLs:
   - Slash Commands → `/roi` → Request URL
   - Slash Commands → `/roi-help` → Request URL  
   - Event Subscriptions → Request URL
   - Interactivity → Request URL

## Step 6: Test Your Bot

1. Start your bot: `python3 roi-slackbot.py`
2. Invite bot to a channel: `/invite @ROI Graph Generator`
3. Test the command: `/roi VR training vs traditional over 2 years`

## Troubleshooting

- **"URL verification failed"**: Make sure ngrok is running and URLs are updated
- **"Not in channel"**: Invite the bot to your channel
- **"Permission denied"**: Check that all scopes are properly configured

## What the Bot Does

- `/roi [description]` - Generates ROI graphs from natural language
- `/roi-help` - Shows help information
- Responds to mentions with helpful information
- Uploads generated graphs directly to Slack channels

Ready to test! 🎯
