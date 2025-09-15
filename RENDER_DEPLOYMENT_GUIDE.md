# 🚀 Render Deployment Guide for ROI Slack Bot

## ✅ Files Ready for Deployment:
- ✅ `Procfile` - Tells Render how to run your app
- ✅ `runtime.txt` - Specifies Python version
- ✅ `requirements.txt` - Python dependencies
- ✅ `.gitignore` - Prevents committing sensitive files
- ✅ Clean git repository (no API keys in history)

## 🌐 Deploy via Render (100% Free!):

### Step 1: Create Render Account
1. Go to: https://render.com/
2. Click "Get Started for Free"
3. Sign up with GitHub (recommended)
4. Authorize Render to access your GitHub

### Step 2: Create New Web Service
1. In Render dashboard, click "New +"
2. Select "Web Service"
3. Connect your GitHub account if not already connected
4. Find and select: `fromdehart/roi-slack-bot`
5. Click "Connect"

### Step 3: Configure Your Service
1. **Name:** `roi-slack-bot` (or whatever you prefer)
2. **Environment:** `Python 3`
3. **Build Command:** `pip install -r requirements.txt`
4. **Start Command:** `gunicorn roi-slackbot:flask_app`
5. **Plan:** Select "Free" plan
6. Click "Create Web Service"

### Step 4: Set Environment Variables
1. In your Render service dashboard, go to "Environment" tab
2. Add these environment variables:
   - `OPENAI_API_KEY` = your_openai_api_key_here
   - `SLACK_BOT_TOKEN` = your_slack_bot_token_here
   - `SLACK_SIGNING_SECRET` = your_slack_signing_secret_here

### Step 5: Deploy
1. Render will automatically start building and deploying
2. Wait for deployment to complete (usually 2-3 minutes)
3. You'll see a URL like: `https://roi-slack-bot.onrender.com`

### Step 6: Update Slack App URLs
1. Go to your Slack app dashboard: https://api.slack.com/apps
2. Update these URLs with your Render URL:
   - **Slash Commands** → `/roi` → Request URL: `https://roi-slack-bot.onrender.com/slack/events`
   - **Slash Commands** → `/roi-help` → Request URL: `https://roi-slack-bot.onrender.com/slack/events`
   - **Event Subscriptions** → Request URL: `https://roi-slack-bot.onrender.com/slack/events`
   - **Interactivity** → Request URL: `https://roi-slack-bot.onrender.com/slack/events`

### Step 7: Test Your Live Bot!
Try the command in Slack: `/roi VR training vs traditional over 2 years`

## 🎯 Your bot will be live at:
`https://roi-slack-bot.onrender.com`

## 💰 Render Free Tier:
- **100% FREE** - No credit card required
- **750 hours/month** - Enough for always-on service
- **512MB RAM** - Plenty for your bot
- **Auto-sleep** after 15 minutes of inactivity (wakes up on request)

## 📝 Render Advantages:
- ✅ **Completely free**
- ✅ **One-click GitHub deployment**
- ✅ **Automatic HTTPS**
- ✅ **Easy environment variable management**
- ✅ **Automatic deployments on git push**
- ✅ **Great for Python Flask apps**
- ✅ **No credit card required**

## 🔧 Troubleshooting:
- **If deployment fails:** Check the Render logs in the dashboard
- **If Slack can't reach it:** Verify the Render URL is correct
- **If environment variables aren't working:** Make sure they're set in Render dashboard
- **If app sleeps:** First request after sleep takes ~30 seconds to wake up

## 🎉 Success!
Once deployed, your ROI Slack bot will be:
- ✅ **Live 24/7**
- ✅ **Handling multiple users**
- ✅ **Generating professional ROI graphs**
- ✅ **Running on Render's infrastructure**
- ✅ **Completely free!**

Ready to deploy? 🚀
