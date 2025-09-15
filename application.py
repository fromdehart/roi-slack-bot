#!/usr/bin/env python3
"""
AWS Elastic Beanstalk entry point for ROI Slack Bot
"""

# Import the Flask app from our main module
import importlib.util
import sys

# Load the roi-slackbot module (note the hyphen in filename)
spec = importlib.util.spec_from_file_location("roi_slackbot", "roi-slackbot.py")
roi_slackbot = importlib.util.module_from_spec(spec)
sys.modules["roi_slackbot"] = roi_slackbot
spec.loader.exec_module(roi_slackbot)

flask_app = roi_slackbot.flask_app

# AWS Elastic Beanstalk looks for 'application' variable
application = flask_app

if __name__ == "__main__":
    # For local testing
    application.run(debug=False, host="0.0.0.0", port=5000)
