# 🚀 Quick Start Guide - Agentic RAG System

## 📋 Prerequisites

1. **Python 3.10+** installed
2. **LightRAG Service** running on `http://localhost:9621`
3. **OpenAI API Key**
4. **Tavily API Key** (optional, for web search)

## ⚡ Quick Setup (5 minutes)

### 1. Install Dependencies

**Option A: Using pip (Recommended for quick start)**
```bash
cd /mnt/d/Workspace/agentic/agent
pip install -r requirements.txt
```

**Option B: Using Poetry**
```bash
cd /mnt/d/Workspace/agentic/agent
poetry install
```

### 2. Environment Configuration

Create `.env` file:
```bash
cp .env.example .env
```

Edit `.env` with your API keys:
```env
# Required
OPENAI_API_KEY=your_openai_key_here

# Optional
TAVILY_API_KEY=your_tavily_key_here

# LightRAG Configuration
LIGHTRAG_URL=http://localhost:9621
LIGHT_RAG_HOST=http://localhost:9621/query

# Workflow Settings
MAX_RETRIES=2
ACCEPTANCE_THRESHOLD=0.7
TEMPERATURE=0.3
MAX_TOKENS=500
```

### 3. Start LightRAG Service

Make sure LightRAG is running on port 9621:
```bash
# Test if LightRAG is running
curl -X POST http://localhost:9621/query \
  -H "Content-Type: application/json" \
  -d '{"query":"test","mode":"hybrid"}'
```

### 4. Run the Agent

**Option A: Direct Python**
```bash
cd /mnt/d/Workspace/agentic/agent
python src/main.py
```

**Option B: Using Poetry**
```bash
cd /mnt/d/Workspace/agentic/agent
poetry run python src/main.py
```

## 🧪 Test the System

### Basic Test
```python
# Test the enhanced RAG query
python -c "
import asyncio
from src.agent import agent

async def test():
    response = await agent.run('What is machine learning?')
    print(f'Response: {response}')

asyncio.run(test())
"
```

### Frontend Test (if UI is running)
```bash
cd /mnt/d/Workspace/agentic/ui
npm install
npm run dev
```

## 📊 Expected Workflow Output

When you run a query, you should see:
```
🎯 STEP 1: START
   📝 Query: What is machine learning?

🤖 STEP 2: LLM Agent - Rewrite the initial query
   ✏️ Rewritten: Comprehensive explanation of machine learning concepts...

📝 STEP 3: Updated query
   📋 Query: ...

🤖 STEP 4: LLM Agent - Do I need more details?
   ✅ YES - Need more details, proceeding to source selection

🤖 STEP 5: LLM Agent - Which source will help?
   🎯 Selected source: vector_database

📚 STEP 6: Retrieving from sources
   🗄️ Querying Vector Database
   ✅ Retrieved X results

📄 STEP 7: Retrieved context
   📋 Context compiled from X sources

📝 STEP 8: Updated query
   🔄 Enhanced query prepared for response generation

🤖 STEP 9: LLM generating response
   💬 Response generated

🤖 STEP 10: LLM Agent - Is the answer relevant?
   ✅ YES - Answer is relevant (score: 0.85)

🎉 STEP 11: Final response
   ✅ Workflow completed successfully!
```

## 🔧 Troubleshooting

### Common Issues

1. **Import Errors**
   ```bash
   cd /mnt/d/Workspace/agentic/agent
   export PYTHONPATH=$PYTHONPATH:/mnt/d/Workspace/agentic/agent/src
   ```

2. **LightRAG Connection Error**
   - Ensure LightRAG is running on port 9621
   - Check firewall settings
   - Verify `LIGHTRAG_URL` in `.env`

3. **OpenAI API Error**
   - Verify API key in `.env`
   - Check API quota/billing

4. **Poetry Errors**
   - Use pip instead: `pip install -r requirements.txt`

### Debug Mode
```bash
# Run with debug logging
export LOG_LEVEL=DEBUG
python src/main.py
```

## 🎯 Next Steps

1. **Add Documents to LightRAG**: Use the document indexing tools
2. **Customize Prompts**: Edit system prompts in `src/agent.py`
3. **Adjust Thresholds**: Modify acceptance threshold in `.env`
4. **Frontend Integration**: Connect with CopilotKit UI

## 📚 Documentation

- `WORKFLOW_DIAGRAM_COMPLIANCE.md` - Complete workflow documentation
- `PYDANTIC_AI_MIGRATION.md` - Technical implementation details
- `LIGHTRAG_INTEGRATION.md` - LightRAG service integration

## ✅ Success Indicators

You know the system is working when:
- ✅ All 12 workflow steps execute
- ✅ LightRAG responses are received
- ✅ Quality scores are above threshold
- ✅ Final responses are generated

Ready to go! 🚀