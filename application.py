#!/usr/bin/env python3
"""
AWS Elastic Beanstalk entry point for ROI Slack Bot
"""

# Import the Flask app from our main module
from roi_slackbot import flask_app

# AWS Elastic Beanstalk looks for 'application' variable
application = flask_app

if __name__ == "__main__":
    # For local testing
    application.run(debug=False, host="0.0.0.0", port=5000)
