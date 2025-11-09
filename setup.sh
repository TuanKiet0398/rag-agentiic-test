#!/bin/bash

echo "🚀 Setting up Agentic RAG System..."

# Navigate to agent directory
cd agent || exit 1

echo "📦 Installing Python dependencies..."
# Install Python dependencies using uv (or pip if uv not available)
if command -v uv &> /dev/null; then
    uv sync
else
    echo "⚠️  uv not found, using pip..."
    pip install -e .
fi

# Check if .env file exists, create from example if not
if [ ! -f .env ]; then
    echo "📝 Creating .env file from template..."
    cp .env.example .env
    echo "⚠️  Please edit .env file with your API keys:"
    echo "   - OPENAI_API_KEY=your_openai_api_key"
    echo "   - TAVILY_API_KEY=your_tavily_api_key" 
fi

# Navigate back and install frontend dependencies
cd ..

echo "🎨 Installing frontend dependencies..."
npm install

echo "✅ Setup complete!"
echo ""
echo "🔧 To run the system:"
echo "   1. Edit agent/.env with your API keys"
echo "   2. Run: npm run dev"
echo ""
echo "📋 Available commands:"
echo "   npm run dev        - Start both frontend and backend"
echo "   npm run dev:agent  - Start backend only"
echo "   npm run dev:ui     - Start frontend only"
echo ""
echo "🌐 Access points:"
echo "   Frontend: http://localhost:3000"
echo "   Backend:  http://localhost:8000"
echo "   AG-UI:    http://localhost:8000/ui"