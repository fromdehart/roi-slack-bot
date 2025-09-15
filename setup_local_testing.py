#!/usr/bin/env python3
"""
Setup script for local testing
This script helps you set up the environment for local testing
"""

import os
import subprocess
import sys

def create_env_file():
    """Create .env file from template"""
    env_example_path = ".env.example"
    env_path = ".env"
    
    if os.path.exists(env_path):
        print("✅ .env file already exists")
        return True
    
    if not os.path.exists(env_example_path):
        print("❌ .env.example file not found")
        return False
    
    try:
        # Copy .env.example to .env
        with open(env_example_path, 'r') as src, open(env_path, 'w') as dst:
            dst.write(src.read())
        
        print("✅ Created .env file from template")
        print("📝 Please edit .env file and add your OpenAI API key")
        return True
    except Exception as e:
        print(f"❌ Error creating .env file: {str(e)}")
        return False

def install_dependencies():
    """Install required Python packages"""
    print("📦 Installing dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error installing dependencies: {str(e)}")
        return False

def check_openai_key():
    """Check if OpenAI API key is configured"""
    from dotenv import load_dotenv
    load_dotenv()
    
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key or api_key == "your_openai_api_key_here":
        print("⚠️  OpenAI API key not configured")
        print("Please edit .env file and add your actual OpenAI API key")
        return False
    else:
        print("✅ OpenAI API key is configured")
        return True

def main():
    print("🚀 Setting up local testing environment...")
    print("=" * 50)
    
    # Step 1: Create .env file
    if not create_env_file():
        return False
    
    # Step 2: Install dependencies
    if not install_dependencies():
        return False
    
    # Step 3: Check OpenAI key
    openai_configured = check_openai_key()
    
    print("\n" + "=" * 50)
    if openai_configured:
        print("🎉 Setup complete! You can now run: python test_graph_generation.py")
    else:
        print("📝 Please configure your OpenAI API key in .env file, then run:")
        print("   python test_graph_generation.py")
    
    return True

if __name__ == "__main__":
    main()

