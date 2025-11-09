#!/bin/bash
# Agentic RAG System - Setup and Start Script

echo "🚀 Starting Agentic RAG System Setup..."

# Check if we're in the right directory
if [ ! -f "pyproject.toml" ]; then
    echo "❌ Error: Please run this script from the agent directory"
    echo "   Expected location: d:/Workspace/agentic/agent/"
    exit 1
fi

echo "📦 Installing dependencies with Poetry..."

# Install poetry if not available
if ! command -v poetry &> /dev/null; then
    echo "🔧 Installing Poetry..."
    curl -sSL https://install.python-poetry.org | python3 -
    export PATH="$HOME/.local/bin:$PATH"
fi

# Install dependencies
poetry install

echo "🔧 Setting up environment..."

# Create .env file if it doesn't exist
if [ ! -f ".env" ]; then
    echo "📝 Creating .env file..."
    cp .env.example .env
    echo "⚠️  Please edit .env file and add your API keys:"
    echo "   - OPENAI_API_KEY=your_openai_key"
    echo "   - TAVILY_API_KEY=your_tavily_key"
    echo "   - LIGHTRAG_URL=http://localhost:9621"
fi

echo "✅ Setup complete!"
echo ""
echo "🎯 Next steps:"
echo "1. Edit .env file with your API keys"
echo "2. Make sure LightRAG is running on http://localhost:9621"
echo "3. Run: poetry run python src/main.py"
echo ""
echo "📚 For more details, see: STARTUP_GUIDE.md"