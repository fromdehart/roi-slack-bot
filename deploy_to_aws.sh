#!/bin/bash

# AWS Deployment Script for ROI Slack Bot
echo "🚀 Preparing ROI Slack Bot for AWS deployment..."

# Check if AWS CLI is installed
if ! command -v aws &> /dev/null; then
    echo "❌ AWS CLI not found. Please install it first:"
    echo "   brew install awscli  # on macOS"
    echo "   pip install awscli   # or via pip"
    exit 1
fi

# Check if EB CLI is installed
if ! command -v eb &> /dev/null; then
    echo "❌ Elastic Beanstalk CLI not found. Please install it first:"
    echo "   pip install awsebcli"
    exit 1
fi

echo "✅ AWS tools found"

# Create deployment package
echo "📦 Creating deployment package..."

# Remove old deployment files
rm -f roi-slack-bot-aws.zip

# Create zip file (excluding files in .ebignore)
zip -r roi-slack-bot-aws.zip . -x@.ebignore

echo "✅ Deployment package created: roi-slack-bot-aws.zip"

# Check if we're in an EB environment
if [ ! -f ".elasticbeanstalk/config.yml" ]; then
    echo "🔧 Initializing Elastic Beanstalk environment..."
    echo "Please run: eb init"
    echo "Then run: eb create roi-slack-bot-env"
    echo "Finally run: eb deploy"
else
    echo "🚀 Deploying to AWS Elastic Beanstalk..."
    eb deploy
fi

echo "✅ Deployment complete!"
echo "🌐 Your app will be available at the URL shown in the output above"
echo "📝 Don't forget to:"
echo "   1. Set environment variables in AWS Console"
echo "   2. Update your Slack app URLs"
echo "   3. Test the /roi command"
