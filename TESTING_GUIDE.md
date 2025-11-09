# 🧪 Agentic RAG System - Testing Guide

## System Overview

This 12-step Agentic RAG system processes queries through a sophisticated workflow with LightRAG integration:

1. **Query Rewrite** - Optimize and clarify queries
2. **Source Selection** - Choose best data sources (LightRAG, web, APIs)
3. **Retrieval** - Get relevant information from LightRAG knowledge base
4. **Context Compilation** - Organize and merge retrieved data
5. **Response Generation** - Create comprehensive answers
6. **Quality Validation** - Self-grade with detailed rubrics
7. **Quality Control Loops** - Retry mechanisms for improvement

### LightRAG Integration Features:
- **Document Processing & Indexing** - Add documents to knowledge base
- **Advanced Retrieval Modes** - Local, global, and hybrid search
- **Entity & Relationship Extraction** - Automated knowledge graph building
- **Real-time Knowledge Base Expansion** - Dynamic document addition

## 🚀 Quick Start

1. **Setup Environment:**
   ```bash
   # Run setup script
   ./setup.sh        # Linux/Mac
   setup.bat         # Windows
   
   # Or manually:
   cd agent && uv sync && cd ..
   npm install
   ```

2. **Configure API Keys and LightRAG:**
   Edit `agent/.env` file:
   ```env
   OPENAI_API_KEY=your_openai_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here
   LIGHTRAG_URL=http://localhost:9621
   ```
   
   **Start LightRAG Service:**
   Make sure your LightRAG service is running on http://localhost:9621

3. **Start System:**
   ```bash
   npm run dev  # Starts both frontend and backend
   ```

4. **Access Interface:**
   - Frontend: http://localhost:3000
   - Backend AG-UI: http://localhost:8000/ui

## 📋 Test Cases

### Test Case 1: Simple Factual Query
**Query:** "What is machine learning?"
**Expected:** Should use LightRAG local mode, provide comprehensive explanation with high confidence

### Test Case 1b: Document Indexing
**Query:** "Add this document to the knowledge base: 'Neural networks are computing systems inspired by biological neural networks.'"
**Expected:** Should successfully index document and confirm addition

### Test Case 2: Current Events Query
**Query:** "What are the latest AI developments in 2024?"
**Expected:** Should route to web search, get recent information

### Test Case 3: Calculation Query
**Query:** "Calculate 15 * 24 + 37"
**Expected:** Should use API tools, return mathematical result

### Test Case 4: Complex Domain Query
**Query:** "Compare deep learning vs traditional machine learning"
**Expected:** Should use LightRAG global mode, compile context from knowledge base, provide detailed comparison

### Test Case 5: Knowledge Base Status
**Query:** "Check the knowledge base status"
**Expected:** Should return LightRAG statistics and connection status

### Test Case 6: Abbreviation Expansion
**Query:** "What's ML and DL?"
**Expected:** Query rewriter should expand to "Machine Learning and Deep Learning"

### Test Case 7: Quality Control Test
**Query:** "Tell me about xyz123invalid"
**Expected:** Should detect poor context quality, potentially retry or indicate low confidence

## 🔍 Monitoring Workflow Steps

The system provides detailed feedback on each step:

### Frontend Monitoring
- **RAG Card Display:** Shows recent queries and responses with confidence scores
- **Quality Scores:** Displays relevancy, faithfulness, context quality, coherence
- **Source Attribution:** Shows which sources were used
- **Metadata:** Includes retrieval method and query rewrite count

### Backend Monitoring (AG-UI)
- **Step-by-Step Progress:** Real-time workflow execution
- **Tool Calls:** Detailed logs of each retrieval operation
- **Agent State:** Current workflow state and history

## 🎯 Expected Behaviors

### High-Quality Responses
- **Confidence ≥ 80%:** Direct, complete answers with excellent source material
- **All Quality Scores ≥ 70%:** Relevant, faithful, coherent responses
- **Source Attribution:** Clear indication of information sources

### Medium-Quality Responses  
- **Confidence 60-79%:** Good answers but may have minor gaps
- **Some Quality Scores < 70%:** May trigger retry mechanisms
- **Partial Context:** Acknowledges limitations in available information

### Low-Quality Responses
- **Confidence < 60%:** Limited or uncertain answers
- **Multiple Retries:** System attempts to improve through different approaches
- **Disclaimers:** Clear indication of uncertainty

## 🔧 Debugging Common Issues

### Backend Issues
1. **OpenAI API Errors:**
   - Check API key in `.env`
   - Verify account has sufficient credits
   - Check internet connectivity

2. **ChromaDB Errors:**
   - Ensure `./vector_db` directory exists
   - Check write permissions
   - Vector database starts empty (normal)

3. **Tavily API Errors:**
   - Verify Tavily API key
   - Check Tavily service status
   - Web search will fallback gracefully

### Frontend Issues
1. **CopilotKit Connection:**
   - Ensure backend is running on port 8000
   - Check `/api/copilotkit` route configuration
   - Verify agent name matches ("my_agent")

2. **State Management:**
   - Check browser console for errors
   - Verify agent state structure matches types
   - Clear browser cache if needed

## 📊 Performance Metrics

### Response Quality Targets
- **Relevancy Score:** ≥ 70%
- **Faithfulness Score:** ≥ 80%  
- **Context Quality:** ≥ 70%
- **Coherence Score:** ≥ 75%
- **Overall Confidence:** ≥ 70%

### System Performance
- **Query Processing Time:** < 10 seconds typical
- **Retry Attempts:** Maximum 2 per query
- **Success Rate:** ≥ 95% with proper API configuration

## 🧪 Advanced Testing

### Load Testing
```bash
# Test multiple concurrent queries
for i in {1..5}; do
  curl -X POST http://localhost:8000/query \
    -H "Content-Type: application/json" \
    -d '{"query": "What is artificial intelligence?"}' &
done
```

### API Testing
```bash
# Direct backend API test
curl -X POST http://localhost:8000/query \
  -H "Content-Type: application/json" \
  -d '{"query": "Explain machine learning"}'
```

## 🎓 Learning Outcomes

After testing, you should understand:

1. **Query Optimization:** How the system rewrites queries for better retrieval
2. **Source Intelligence:** How it selects appropriate data sources  
3. **Quality Assurance:** How self-grading improves response quality
4. **Retry Mechanisms:** How the system handles low-quality initial responses
5. **Multi-Modal Retrieval:** Integration of vector DB, web search, and APIs
6. **State Management:** How CopilotKit manages agent state across interactions

## 🔄 Continuous Improvement

The system is designed for extensibility:

- **Add New Sources:** Extend `tools.py` with additional APIs
- **Enhance Quality Metrics:** Modify grading criteria in main agent
- **Custom Retrieval Methods:** Add specialized retrievers for domain knowledge
- **Frontend Customization:** Extend React components for better UX
- **Monitoring Integration:** Add logging and analytics for production use

## 🎯 Success Criteria

A successful test deployment demonstrates:

✅ **Functional 12-Step Workflow:** All steps execute without errors
✅ **Quality Control:** System identifies and improves low-quality responses  
✅ **Multi-Source Retrieval:** Successfully uses vector DB, web search, and APIs
✅ **Intelligent Routing:** Selects appropriate sources based on query type
✅ **Frontend Integration:** CopilotKit displays results with proper metadata
✅ **State Persistence:** Agent maintains conversation history and context
✅ **Error Handling:** Graceful degradation when external services fail