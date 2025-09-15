# 🚀 AWS Elastic Beanstalk Deployment Guide

## Overview
We'll deploy your ROI Slack Bot to AWS Elastic Beanstalk using the free tier. This is more reliable than Render and has better Python support.

## Prerequisites
- AWS Account (free tier eligible)
- Your GitHub repository with the code
- Slack app credentials ready

## Step 1: Create AWS Account
1. Go to [aws.amazon.com](https://aws.amazon.com)
2. Click "Create an AWS Account"
3. Follow the signup process
4. **Important**: Choose "Personal" account type to get free tier
5. Add a credit card (won't be charged for free tier usage)

## Step 2: Access Elastic Beanstalk
1. Log into AWS Console
2. Search for "Elastic Beanstalk" in the services search
3. Click on "Elastic Beanstalk"

## Step 3: Create Application
1. Click "Create Application"
2. **Application name**: `roi-slack-bot`
3. **Platform**: Python 3.9
4. **Platform branch**: Python 3.9 running on 64bit Amazon Linux 2
5. **Platform version**: Latest
6. **Application code**: Upload your code

## Step 4: Prepare Your Code for AWS

### Create Application Files
You'll need these additional files in your repository:

#### `.ebextensions/01_packages.config`
```yaml
packages:
  yum:
    gcc: []
    python3-devel: []
    libffi-devel: []
    openssl-devel: []
```

#### `application.py` (AWS entry point)
```python
from roi_slackbot import flask_app

# This is the entry point for AWS Elastic Beanstalk
application = flask_app

if __name__ == "__main__":
    application.run()
```

## Step 5: Update Your Repository

### Files to Add/Modify:
1. **Create `.ebextensions/` folder** with package configuration
2. **Create `application.py`** as the entry point
3. **Update `requirements.txt`** if needed

## Step 6: Deploy to AWS

### Option A: Upload ZIP File
1. Create a ZIP file of your entire project
2. In Elastic Beanstalk, choose "Upload your code"
3. Select the ZIP file
4. Click "Create environment"

### Option B: Use AWS CLI (Advanced)
1. Install AWS CLI
2. Configure with your credentials
3. Use `eb init` and `eb deploy` commands

## Step 7: Configure Environment Variables
1. In your Elastic Beanstalk environment dashboard
2. Go to **Configuration** → **Software**
3. Add these environment variables:
   - `SLACK_BOT_TOKEN`: Your bot token (xoxb-...)
   - `SLACK_SIGNING_SECRET`: Your signing secret
   - `OPENAI_API_KEY`: Your OpenAI API key

## Step 8: Update Slack App URLs
1. Once deployed, you'll get a URL like: `http://roi-slack-bot-env.region.elasticbeanstalk.com`
2. Update your Slack app with this URL:
   - **Request URL**: `http://your-app-url/slack/events`
   - **Slash Command URLs**: `http://your-app-url/slack/events`

## Step 9: Test Your Deployment
1. Visit your app URL in browser
2. You should see: "ROI Graph Generator Bot - Status: ✅ Running"
3. Test `/roi` command in Slack

## Troubleshooting

### Common Issues:
1. **Import errors**: Check that all dependencies are in `requirements.txt`
2. **Environment variables**: Ensure they're set in Elastic Beanstalk configuration
3. **Slack URL verification**: Make sure your app URL is accessible from internet

### Logs:
- View logs in Elastic Beanstalk dashboard under "Logs"
- Download logs to debug issues

## Cost Management
- **Free tier**: 750 hours/month of t2.micro instances
- **Your app**: Will likely use ~720 hours/month (24/7)
- **Cost**: Should be $0 for the first 12 months

## Security Notes
- Environment variables are encrypted in AWS
- No need to commit secrets to Git
- AWS handles SSL certificates automatically

## Next Steps After Deployment
1. Test all Slack commands
2. Monitor AWS CloudWatch for performance
3. Set up monitoring alerts if needed
4. Consider adding custom domain later

---

**Ready to start?** Let me know when you have your AWS account set up and I'll help you create the deployment files!
