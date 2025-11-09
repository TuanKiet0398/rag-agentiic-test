#!/usr/bin/env python3
"""
Quick Start Script for Agentic RAG System
Run this to verify your setup and test the system
"""

import os
import sys
import asyncio
import subprocess
import json
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 10):
        print("❌ Python 3.10+ required. Current version:", sys.version)
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True

def check_env_file():
    """Check if .env file exists and has required keys"""
    env_path = Path(".env")
    if not env_path.exists():
        print("❌ .env file not found. Copy from .env.example and configure:")
        print("   cp .env.example .env")
        return False
    
    required_keys = ["OPENAI_API_KEY", "LIGHTRAG_URL"]
    missing_keys = []
    
    try:
        with open(env_path) as f:
            env_content = f.read()
            for key in required_keys:
                if f"{key}=" not in env_content or f"{key}=your_" in env_content:
                    missing_keys.append(key)
        
        if missing_keys:
            print(f"❌ Missing or unconfigured keys in .env: {missing_keys}")
            return False
        
        print("✅ .env file configured")
        return True
    except Exception as e:
        print(f"❌ Error reading .env file: {e}")
        return False

def check_lightrag_service():
    """Check if LightRAG service is running"""
    import requests
    try:
        response = requests.post(
            "http://localhost:9621/query",
            json={"query": "test", "mode": "hybrid"},
            timeout=5
        )
        if response.status_code == 200:
            print("✅ LightRAG service running on localhost:9621")
            return True
        else:
            print(f"❌ LightRAG service error: {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ LightRAG service not running on localhost:9621")
        print("   Please start your LightRAG service first")
        return False
    except Exception as e:
        print(f"❌ LightRAG check failed: {e}")
        return False

def install_dependencies():
    """Install required Python packages"""
    try:
        print("📦 Installing Python dependencies...")
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                      check=True, capture_output=True)
        print("✅ Dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

async def test_agent():
    """Test the agent system"""
    try:
        print("🧪 Testing Agentic RAG system...")
        
        # Import after dependencies are installed
        from src.agent import AgenticRAGProcessor
        from src.tools import RAGDeps
        
        processor = AgenticRAGProcessor()
        deps = RAGDeps()
        
        result = await processor.process_query_workflow(
            "What is artificial intelligence?", 
            deps
        )
        
        print("✅ Agent test successful!")
        print(f"   Answer preview: {result.answer[:100]}...")
        print(f"   Confidence: {result.confidence:.2f}")
        print(f"   Sources: {len(result.sources)}")
        return True
        
    except Exception as e:
        print(f"❌ Agent test failed: {e}")
        return False

def check_frontend():
    """Check if frontend dependencies are available"""
    frontend_path = Path("../src/package.json")
    if not frontend_path.exists():
        print("⚠️  Frontend not found in ../src/")
        return False
    
    print("✅ Frontend directory found")
    print("   To start frontend:")
    print("   cd ../src && npm install && npm run dev")
    return True

async def main():
    """Main startup sequence"""
    print("🚀 Agentic RAG System Startup Check")
    print("=" * 40)
    
    checks = []
    
    # 1. Python version
    checks.append(check_python_version())
    
    # 2. Environment file  
    checks.append(check_env_file())
    
    # 3. Dependencies
    if checks[-1]:  # Only if env file is ok
        checks.append(install_dependencies())
    
    # 4. LightRAG service
    if checks[-1]:  # Only if deps are installed
        checks.append(check_lightrag_service())
    
    # 5. Agent test
    if all(checks):
        checks.append(await test_agent())
    
    # 6. Frontend check
    check_frontend()
    
    print("\n" + "=" * 40)
    if all(checks):
        print("🎉 System Ready!")
        print("\nNext steps:")
        print("1. Start backend: python -m uvicorn src.main:app --reload")
        print("2. Start frontend: cd ../src && npm run dev")
        print("3. Open browser: http://localhost:3000")
    else:
        print("❌ Setup incomplete. Please fix the issues above.")
        return 1
    
    return 0

if __name__ == "__main__":
    # Change to agent directory if not already there
    if "agent" not in str(Path.cwd()):
        agent_path = Path("agent")
        if agent_path.exists():
            os.chdir(agent_path)
            print(f"📁 Changed to {Path.cwd()}")
    
    exit_code = asyncio.run(main())
    sys.exit(exit_code)