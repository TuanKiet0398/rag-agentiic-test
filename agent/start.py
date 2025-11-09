#!/usr/bin/env python3
"""
Simple startup script for Agentic RAG System
Works with both Poetry and pip installations
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 10):
        print("❌ Error: Python 3.10+ is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def check_env_file():
    """Check if .env file exists"""
    env_file = Path(".env")
    if not env_file.exists():
        print("⚠️  .env file not found. Creating from .env.example...")
        example_file = Path(".env.example")
        if example_file.exists():
            with open(example_file, 'r') as f:
                content = f.read()
            with open(env_file, 'w') as f:
                f.write(content)
            print("✅ .env file created. Please update with your API keys.")
        else:
            print("❌ .env.example not found. Please create .env manually.")
            return False
    else:
        print("✅ .env file found")
    return True

def install_dependencies():
    """Install dependencies using Poetry or pip"""
    print("\n📦 Installing dependencies...")
    
    # Try Poetry first
    try:
        result = subprocess.run(["poetry", "--version"], 
                              capture_output=True, text=True, check=True)
        print(f"✅ Found Poetry: {result.stdout.strip()}")
        
        print("🔧 Installing with Poetry...")
        subprocess.run(["poetry", "install"], check=True)
        return "poetry"
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("⚠️  Poetry not found or failed. Trying pip...")
        
        # Fall back to pip
        try:
            subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], check=True)
            print("✅ Dependencies installed with pip")
            return "pip"
        except subprocess.CalledProcessError as e:
            print(f"❌ Failed to install dependencies: {e}")
            return None

def start_agent():
    """Start the Agentic RAG agent"""
    print("\n🚀 Starting Agentic RAG Agent...")
    
    try:
        # Import and run the main function
        from src.main import main
        main()
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("   Make sure dependencies are installed correctly")
        return False
    except Exception as e:
        print(f"❌ Error starting agent: {e}")
        return False
    
    return True

def main():
    """Main startup function"""
    print("🎯 Agentic RAG System - Startup Script")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        return
    
    # Check .env file
    if not check_env_file():
        return
    
    # Install dependencies
    install_method = install_dependencies()
    if not install_method:
        return
    
    print(f"\n✅ Setup complete using {install_method}!")
    print("\n📋 Next steps:")
    print("1. Update .env file with your API keys:")
    print("   - OPENAI_API_KEY=your_openai_key")
    print("   - TAVILY_API_KEY=your_tavily_key")
    print("2. Make sure LightRAG is running on http://localhost:9621")
    print("3. Run the agent!")
    
    # Ask if user wants to start the agent
    try:
        response = input("\nStart the agent now? (y/N): ").strip().lower()
        if response in ['y', 'yes']:
            start_agent()
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")

if __name__ == "__main__":
    main()