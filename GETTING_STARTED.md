# 🚀 Getting Started with Agentic RAG System

## Quick Start Guide

This guide will help you start the complete Agentic RAG system with LightRAG integration and the 12-step workflow.

## 📋 Prerequisites

### 1. Required Services
- **LightRAG Service**: Must be running on `http://localhost:9621`
- **OpenAI API**: For GPT-4 models
- **Python 3.10+**: For the backend agent
- **Node.js 18+**: For the frontend UI

### 2. API Keys Required
```bash
# Required environment variables
OPENAI_API_KEY=your_openai_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here  # Optional: for web search
LIGHTRAG_URL=http://localhost:9621
LIGHT_RAG_HOST=http://localhost:9621/query
```

## 🚀 Step-by-Step Startup

### Step 1: Start LightRAG Service
First, ensure your LightRAG service is running:

```bash
# Verify LightRAG is running
curl -X POST http://localhost:9621/query \
  -H "Content-Type: application/json" \
  -d '{"query":"test","mode":"hybrid"}'
```

### Step 2: Setup Backend (Agent)

```bash
# Navigate to agent directory
cd d:\Workspace\agentic\agent

# Create virtual environment (if not exists)
python -m venv env

# Activate virtual environment
.\env\Scripts\Activate.ps1  # PowerShell
# OR
.\env\Scripts\activate.bat  # Command Prompt

# Install dependencies
pip install -r requirements.txt

# Create .env file
copy .env.example .env

# Edit .env file with your API keys
notepad .env
```

**Required .env configuration:**
```bash
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4o-mini
TEMPERATURE=0.3
MAX_TOKENS=500

# LightRAG Configuration  
LIGHTRAG_URL=http://localhost:9621
LIGHT_RAG_HOST=http://localhost:9621/query

# Optional: Web Search
TAVILY_API_KEY=your_tavily_api_key_here

# Workflow Configuration
MAX_RETRIES=2
ACCEPTANCE_THRESHOLD=0.7
```

### Step 3: Test Backend Agent

```bash
# Test the agent directly
python -c "
from src.agent import AgenticRAGProcessor
from src.tools import RAGDeps
import asyncio

async def test():
    processor = AgenticRAGProcessor()
    deps = RAGDeps()
    result = await processor.process_query_workflow(
        'What is machine learning?', 
        deps
    )
    print('✅ Test successful!')
    print(f'Answer: {result.answer[:100]}...')
    print(f'Confidence: {result.confidence}')

asyncio.run(test())
"
```

### Step 4: Start Backend Server

```bash
# Start the agent server
python -m uvicorn src.main:app --host 0.0.0.0 --port 8000 --reload
```

### Step 5: Setup Frontend (UI)

Open a **new terminal** for the frontend:

```bash
# Navigate to UI directory
cd d:\Workspace\agentic\src

# Install dependencies
npm install
# OR
pnpm install

# Start development server
npm run dev
# OR  
pnpm dev
```

### Step 6: Access the Application

Open your browser and go to:
- **Frontend UI**: http://localhost:3000
- **Backend API**: http://localhost:8000/docs (FastAPI docs)
- **LightRAG Service**: http://localhost:9621 (status check)

## 🧪 Testing the Complete System

### Test 1: Simple Query
Try asking: `"What is artificial intelligence?"`

**Expected workflow:**
```
🎯 STEP 1: START
🤖 STEP 2: LLM Agent - Rewrite the initial query
📝 STEP 3: Updated query  
🤖 STEP 4: LLM Agent - Do I need more details? → YES
🤖 STEP 5: LLM Agent - Which source will help? → vector_database
📚 STEP 6: Retrieving from sources → Vector Database
📄 STEP 7: Retrieved context
📝 STEP 8: Updated query
🤖 STEP 9: LLM generating response
🤖 STEP 10: LLM Agent - Is the answer relevant? → YES
🎉 STEP 11: Final response → ✅ WORKFLOW COMPLETE
```

### Test 2: Document Addition
Add a document to the knowledge base:

```python
# In the UI or via API
await add_document_to_knowledge_base(
    ctx=context,
    text="Machine learning is a subset of AI that enables computers to learn without explicit programming.",
    title="ML Definition",
    source="manual_input"
)
```

### Test 3: Enhanced RAG Query
Use the enhanced RAG query tool:

```python
# Test different modes
await enhanced_rag_query(
    ctx=context,
    query="Compare supervised and unsupervised learning",
    mode="global"  # or "local" or "hybrid"
)
```

## 📁 Project Structure

```
d:\Workspace\agentic\
├── agent/                 # Backend (Pydantic AI)
│   ├── src/
│   │   ├── agent.py      # Main 12-step workflow
│   │   ├── tools.py      # LightRAG & retrieval tools  
│   │   ├── models.py     # Data models
│   │   └── main.py       # FastAPI server
│   ├── requirements.txt   # Python dependencies
│   └── .env              # Environment variables
│
└── src/                   # Frontend (Next.js + CopilotKit)
    ├── app/
    ├── components/        # UI components
    ├── lib/              # Utilities
    ├── package.json      # Node dependencies
    └── next.config.mjs   # Next.js config
```

## 🔧 Troubleshooting

### Issue: LightRAG Connection Error
```bash
# Check if LightRAG is running
curl http://localhost:9621/health

# If not running, start your LightRAG service
# (Follow your LightRAG installation guide)
```

### Issue: OpenAI API Error
```bash
# Verify API key
echo $OPENAI_API_KEY

# Test API connection
curl -H "Authorization: Bearer $OPENAI_API_KEY" \
  https://api.openai.com/v1/models
```

### Issue: Frontend Connection Error
```bash
# Check backend is running
curl http://localhost:8000/health

# Check frontend environment
cat src/.env.local
```

## 📊 Monitoring & Logs

### Backend Logs
- Agent workflow steps are logged with step numbers
- LightRAG API calls are logged  
- Error handling includes detailed stack traces

### Frontend Logs
- CopilotKit integration logs in browser console
- Real-time workflow status updates
- State management logs

## 🎯 Next Steps

1. **Add Documents**: Use the document upload feature to populate LightRAG
2. **Test Workflow**: Try different query types (factual, analytical, comparative)
3. **Monitor Performance**: Check response times and quality scores
4. **Customize Settings**: Adjust temperature, max_retries, acceptance_threshold
5. **Scale Up**: Add more knowledge sources and enhance retrieval

## 🆘 Need Help?

- **Workflow Issues**: Check `WORKFLOW_DIAGRAM_COMPLIANCE.md`
- **LightRAG Integration**: See `LIGHTRAG_INTEGRATION.md`  
- **Pydantic AI Migration**: Review `PYDANTIC_AI_MIGRATION.md`
- **API Documentation**: Visit http://localhost:8000/docs

Ready to start your Agentic RAG journey! 🚀