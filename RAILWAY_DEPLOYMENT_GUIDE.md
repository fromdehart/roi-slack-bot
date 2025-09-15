# 🚀 Railway Deployment Guide for ROI Slack Bot

## ✅ Files Ready for Deployment:
- ✅ `Procfile` - Tells Railway how to run your app
- ✅ `runtime.txt` - Specifies Python version
- ✅ `requirements.txt` - Python dependencies
- ✅ `.gitignore` - Prevents committing sensitive files
- ✅ Clean git repository (no API keys in history)

## 🌐 Deploy via Railway (Free $5/month credit):

### Step 1: Create Railway Account
1. Go to: https://railway.app/
2. Click "Start a New Project"
3. Sign up with GitHub (recommended)
4. Authorize Railway to access your GitHub

### Step 2: Deploy from GitHub
1. Click "Deploy from GitHub repo"
2. Find and select: `fromdehart/roi-slack-bot`
3. Click "Deploy Now"
4. Railway will automatically detect it's a Python app

### Step 3: Set Environment Variables
1. In your Railway project dashboard, go to "Variables" tab
2. Add these environment variables:
   - `OPENAI_API_KEY` = your_openai_api_key_here
   - `SLACK_BOT_TOKEN` = your_slack_bot_token_here
   - `SLACK_SIGNING_SECRET` = your_slack_signing_secret_here

### Step 4: Configure Port (Important!)
1. In Railway dashboard, go to "Settings" tab
2. Under "Environment Variables", add:
   - `PORT` = 3000
3. Railway will automatically set this, but good to verify

### Step 5: Get Your Live URL
1. Railway will give you a URL like: `https://roi-slack-bot-production-xxxx.up.railway.app`
2. Copy this URL - you'll need it for Slack configuration

### Step 6: Update Slack App URLs
1. Go to your Slack app dashboard: https://api.slack.com/apps
2. Update these URLs with your Railway URL:
   - **Slash Commands** → `/roi` → Request URL: `https://your-railway-url.up.railway.app/slack/events`
   - **Slash Commands** → `/roi-help` → Request URL: `https://your-railway-url.up.railway.app/slack/events`
   - **Event Subscriptions** → Request URL: `https://your-railway-url.up.railway.app/slack/events`
   - **Interactivity** → Request URL: `https://your-railway-url.up.railway.app/slack/events`

### Step 7: Test Your Live Bot!
Try the command in Slack: `/roi VR training vs traditional over 2 years`

## 🎯 Your bot will be live at:
`https://your-railway-url.up.railway.app`

## 💰 Railway Pricing:
- **Free tier:** $5 credit monthly (plenty for low traffic)
- **Usage:** ~$0.10/day for a small app like yours
- **Your $5 credit** should last the entire month easily

## 📝 Railway Advantages:
- ✅ **Free $5 monthly credit**
- ✅ **One-click GitHub deployment**
- ✅ **Automatic HTTPS**
- ✅ **Easy environment variable management**
- ✅ **Automatic scaling**
- ✅ **Great for Python Flask apps**

## 🔧 Troubleshooting:
- **If deployment fails:** Check the Railway logs in the dashboard
- **If Slack can't reach it:** Verify the Railway URL is correct
- **If environment variables aren't working:** Make sure they're set in Railway dashboard

## 🎉 Success!
Once deployed, your ROI Slack bot will be:
- ✅ **Live 24/7**
- ✅ **Handling multiple users**
- ✅ **Generating professional ROI graphs**
- ✅ **Running on Railway's infrastructure**

Ready to deploy? 🚀
