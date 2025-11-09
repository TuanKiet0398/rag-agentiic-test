#!/bin/bash

# Clean Installation Script for Agentic RAG System
echo "🔧 Fixing Pydantic AI and Logfire compatibility issues..."

# Navigate to agent directory
cd /mnt/d/Workspace/agentic/agent

# Remove existing problematic packages
echo "📦 Removing incompatible packages..."
pip uninstall -y pydantic-ai-slim logfire pydantic-graph

# Clear pip cache
echo "🧹 Clearing pip cache..."
pip cache purge

# Install specific compatible versions
echo "⬇️ Installing compatible versions..."

# Install logfire first with the right version
pip install "logfire==0.49.0"

# Install pydantic-ai-slim with exact version
pip install "pydantic-ai-slim[ag-ui,openai]==0.0.14"

# Install other dependencies
pip install -r requirements.txt

echo "✅ Installation complete!"
echo ""
echo "🧪 Testing imports..."
python -c "
try:
    from pydantic_ai import Agent
    from pydantic_ai.models.openai import OpenAIResponsesModel
    print('✅ Pydantic AI imports successful')
except Exception as e:
    print(f'❌ Import error: {e}')
"

echo ""
echo "🚀 Ready to start! Run: python src/main.py"