#!/usr/bin/env python3
"""
Safe local testing script for ROI graph generation
This script tests the graph generation functionality without Slack integration
"""

import os
import sys
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def test_graph_generation():
    """Test the graph generation functionality locally"""
    
    # Check if OpenAI API key is set
    openai_key = os.environ.get("OPENAI_API_KEY")
    if not openai_key or openai_key == "your_openai_api_key_here":
        print("❌ Error: OPENAI_API_KEY not set in .env file")
        print("Please add your OpenAI API key to the .env file")
        return False
    
    try:
        # Import the graph generator
        from graph_generator import generate_roi_graph
        
        # Test cases
        test_requests = [
            "VR training vs traditional training ROI over 3 years",
            "Cost savings from VR implementation quarterly breakdown",
            "Employee satisfaction before and after VR training"
        ]
        
        print("🧪 Starting local graph generation tests...")
        print("=" * 50)
        
        for i, request in enumerate(test_requests, 1):
            print(f"\n📊 Test {i}: {request}")
            print("-" * 40)
            
            try:
                # Generate the graph
                image_path = generate_roi_graph(request)
                
                if os.path.exists(image_path):
                    file_size = os.path.getsize(image_path)
                    print(f"✅ Success! Graph saved to: {image_path}")
                    print(f"📁 File size: {file_size:,} bytes")
                    
                    # Clean up the temp file
                    os.remove(image_path)
                    print("🧹 Cleaned up temporary file")
                else:
                    print("❌ Error: Graph file was not created")
                    
            except Exception as e:
                print(f"❌ Error generating graph: {str(e)}")
                logger.error(f"Graph generation failed for '{request}': {str(e)}")
        
        print("\n" + "=" * 50)
        print("🎉 Graph generation testing completed!")
        return True
        
    except ImportError as e:
        print(f"❌ Error importing graph_generator: {str(e)}")
        print("Make sure all dependencies are installed: pip install -r requirements.txt")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        logger.error(f"Unexpected error during testing: {str(e)}")
        return False

def check_dependencies():
    """Check if all required dependencies are available"""
    print("🔍 Checking dependencies...")
    
    required_packages = [
        'matplotlib', 'pandas', 'numpy', 'openai', 'dotenv'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - MISSING")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("Install them with: pip install " + " ".join(missing_packages))
        return False
    else:
        print("✅ All dependencies are available!")
        return True

if __name__ == "__main__":
    print("🚀 ROI Graph Generator - Local Testing")
    print("=" * 50)
    
    # Check dependencies first
    if not check_dependencies():
        print("\n❌ Please install missing dependencies before testing")
        sys.exit(1)
    
    # Test graph generation
    success = test_graph_generation()
    
    if success:
        print("\n🎯 Ready for Slack integration!")
    else:
        print("\n❌ Testing failed. Please check the errors above.")
        sys.exit(1)

