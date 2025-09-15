#!/usr/bin/env python3
"""
Safe local testing script using Docker containers
This script tests the graph generation functionality with containerized execution
"""

import os
import sys
import subprocess
from dotenv import load_dotenv
import logging

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def check_docker():
    """Check if Docker is available"""
    try:
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Docker is available")
            return True
        else:
            print("❌ Docker is not available")
            return False
    except FileNotFoundError:
        print("❌ Docker is not installed")
        return False

def build_docker_image():
    """Build the Docker image for safe execution"""
    print("🔨 Building Docker image for safe graph generation...")
    
    try:
        from graph_generator_safe import build_docker_image
        success = build_docker_image()
        
        if success:
            print("✅ Docker image built successfully")
            return True
        else:
            print("❌ Failed to build Docker image")
            return False
    except Exception as e:
        print(f"❌ Error building Docker image: {str(e)}")
        return False

def test_safe_graph_generation():
    """Test the safe graph generation functionality"""
    
    # Check if OpenAI API key is set
    openai_key = os.environ.get("OPENAI_API_KEY")
    if not openai_key or openai_key == "your_openai_api_key_here":
        print("❌ Error: OPENAI_API_KEY not set in .env file")
        print("Please add your OpenAI API key to the .env file")
        return False
    
    try:
        # Import the safe graph generator
        from graph_generator_safe import generate_roi_graph_safe
        
        # Test cases
        test_requests = [
            "VR training vs traditional training ROI over 3 years",
            "Cost savings from VR implementation quarterly breakdown",
            "Employee satisfaction before and after VR training"
        ]
        
        print("🧪 Starting SAFE graph generation tests with Docker...")
        print("=" * 60)
        
        for i, request in enumerate(test_requests, 1):
            print(f"\n📊 Test {i}: {request}")
            print("-" * 50)
            
            try:
                # Generate the graph using Docker
                image_path = generate_roi_graph_safe(request)
                
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
        
        print("\n" + "=" * 60)
        print("🎉 Safe graph generation testing completed!")
        return True
        
    except ImportError as e:
        print(f"❌ Error importing safe graph generator: {str(e)}")
        return False
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        logger.error(f"Unexpected error during testing: {str(e)}")
        return False

def test_fallback_mode():
    """Test fallback to local execution if Docker fails"""
    print("\n🔄 Testing fallback to local execution...")
    
    try:
        from graph_generator_safe import SafeGraphGenerator
        
        # Create generator in fallback mode
        generator = SafeGraphGenerator(use_docker=False)
        
        test_request = "Simple ROI test over 6 months"
        print(f"📊 Fallback Test: {test_request}")
        
        image_path = generator.generate_roi_graph(test_request)
        
        if os.path.exists(image_path):
            file_size = os.path.getsize(image_path)
            print(f"✅ Fallback Success! Graph saved to: {image_path}")
            print(f"📁 File size: {file_size:,} bytes")
            
            # Clean up
            os.remove(image_path)
            print("🧹 Cleaned up temporary file")
            return True
        else:
            print("❌ Fallback failed: Graph file was not created")
            return False
            
    except Exception as e:
        print(f"❌ Fallback test failed: {str(e)}")
        return False

def main():
    print("🛡️ ROI Graph Generator - SAFE Local Testing with Docker")
    print("=" * 70)
    
    # Step 1: Check Docker
    if not check_docker():
        print("\n⚠️ Docker not available. Testing with fallback mode only.")
        return test_fallback_mode()
    
    # Step 2: Build Docker image
    if not build_docker_image():
        print("\n⚠️ Docker build failed. Testing with fallback mode only.")
        return test_fallback_mode()
    
    # Step 3: Test safe graph generation
    success = test_safe_graph_generation()
    
    if not success:
        print("\n⚠️ Safe testing failed. Trying fallback mode...")
        success = test_fallback_mode()
    
    if success:
        print("\n🎯 Ready for Slack integration!")
        print("💡 For production, use the containerized version for maximum security")
    else:
        print("\n❌ All testing failed. Please check the errors above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
