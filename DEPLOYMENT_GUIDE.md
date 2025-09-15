# 🚀 Heroku Deployment Guide for ROI Slack Bot

## ✅ Files Created for Deployment:
- ✅ `Procfile` - Tells Heroku how to run your app
- ✅ `runtime.txt` - Specifies Python version
- ✅ `requirements.txt` - Python dependencies

## 🌐 Deploy via Heroku Web Interface:

### Step 1: Create Heroku Account
1. Go to: https://signup.heroku.com/
2. Create a free account

### Step 2: Create New App
1. Go to: https://dashboard.heroku.com/new-app
2. App name: `roi-slackbot-yourname` (must be unique)
3. Choose region: United States
4. Click "Create app"

### Step 3: Connect GitHub (Recommended)
1. In your Heroku app dashboard, go to "Deploy" tab
2. Click "Connect to GitHub"
3. Authorize Heroku to access your GitHub
4. Find your repository: `roi-slack-bot`
5. Click "Connect"

### Step 4: Set Environment Variables
1. Go to "Settings" tab in your Heroku app
2. Click "Reveal Config Vars"
3. Add these variables:
   - `OPENAI_API_KEY` = your_openai_api_key_here
   - `SLACK_BOT_TOKEN` = your_slack_bot_token_here  
   - `SLACK_SIGNING_SECRET` = your_slack_signing_secret_here

### Step 5: Deploy
1. Go back to "Deploy" tab
2. Click "Deploy Branch" (main branch)
3. Wait for deployment to complete

### Step 6: Update Slack App URLs
1. Your Heroku app URL will be: `https://roi-slackbot-yourname.herokuapp.com`
2. Update your Slack app settings:
   - Slash Commands: `https://roi-slackbot-yourname.herokuapp.com/slack/events`
   - Event Subscriptions: `https://roi-slackbot-yourname.herokuapp.com/slack/events`

## 🎯 Your bot will be live at:
`https://roi-slackbot-yourname.herokuapp.com`

## 📝 Next Steps:
1. Create Heroku account
2. Create new app
3. Connect GitHub repository
4. Set environment variables
5. Deploy!
6. Update Slack URLs
7. Test your live bot!

Ready to deploy? 🚀
