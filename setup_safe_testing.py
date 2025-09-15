#!/usr/bin/env python3
"""
Setup script for safe local testing with Docker
"""

import os
import subprocess
import sys

def check_docker():
    """Check if Docker is installed and running"""
    try:
        # Check if Docker is installed
        result = subprocess.run(['docker', '--version'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Docker is not installed")
            return False
        
        print(f"✅ Docker installed: {result.stdout.strip()}")
        
        # Check if Docker daemon is running
        result = subprocess.run(['docker', 'info'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Docker daemon is not running")
            print("Please start Docker Desktop or Docker daemon")
            return False
        
        print("✅ Docker daemon is running")
        return True
        
    except FileNotFoundError:
        print("❌ Docker is not installed")
        print("Please install Docker Desktop from: https://www.docker.com/products/docker-desktop")
        return False

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
    print("📦 Installing Python dependencies...")
    
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Python dependencies installed successfully")
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
    print("🛡️ Setting up SAFE local testing environment...")
    print("=" * 60)
    
    # Step 1: Check Docker
    docker_available = check_docker()
    
    # Step 2: Create .env file
    if not create_env_file():
        return False
    
    # Step 3: Install Python dependencies
    if not install_dependencies():
        return False
    
    # Step 4: Check OpenAI key
    openai_configured = check_openai_key()
    
    print("\n" + "=" * 60)
    
    if docker_available and openai_configured:
        print("🎉 Safe setup complete!")
        print("🚀 Run: python3 test_graph_generation_safe.py")
        print("💡 This will use Docker containers for maximum security")
    elif openai_configured:
        print("⚠️  Docker not available, but fallback mode ready")
        print("🚀 Run: python3 test_graph_generation_safe.py")
        print("💡 This will fall back to local execution (less secure)")
    else:
        print("📝 Please configure your OpenAI API key in .env file")
        print("🚀 Then run: python3 test_graph_generation_safe.py")
    
    return True

if __name__ == "__main__":
    main()
