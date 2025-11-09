# Agentic RAG Agent

A sophisticated 12-step Retrieval-Augmented Generation (RAG) system built with Pydantic AI that follows the exact workflow diagram provided.

## Features

- 🤖 **12-Step Workflow**: Follows exact diagram sequence with proper decision points
- 🔄 **Smart Looping**: Automatic retry with query enhancement
- 🎯 **Multi-Source Retrieval**: LightRAG, Web Search, and API integration
- 📊 **Quality Control**: Self-grading with configurable thresholds
- 🔧 **LightRAG Integration**: Advanced knowledge graph capabilities
- 🌐 **Web Search**: Real-time information via Tavily API
- ⚡ **FastAPI Backend**: RESTful API with async processing

## Quick Start

### 1. Install Dependencies
```bash
cd agent
poetry install
```

### 2. Configure Environment
```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Start LightRAG Service
Ensure LightRAG is running on http://localhost:9621

### 4. Run the Agent
```bash
poetry run python -m src.main
```

## Environment Variables

- `OPENAI_API_KEY`: Your OpenAI API key
- `TAVILY_API_KEY`: Your Tavily API key (optional)
- `LIGHTRAG_URL`: LightRAG service URL (default: http://localhost:9621)
- `MAX_RETRIES`: Maximum retry attempts (default: 2)
- `ACCEPTANCE_THRESHOLD`: Quality threshold (default: 0.7)

## Workflow Steps

The system follows a precise 12-step workflow:

1. **START** - Initial query processing
2. **Rewrite Query** - LLM enhances the query
3. **Updated Query** - Display enhanced query
4. **Need Details?** - Decision point (YES→5, NO→12)
5. **Source Selection** - Choose retrieval source
6. **Retrieve** - Get data from selected source
7. **Context** - Compile retrieved information
8. **Update Query** - Enhance with context
9. **Generate Response** - LLM creates answer
10. **Quality Check** - Evaluate relevance (YES→11, NO→12)
11. **Final Response** - Return high-quality answer
12. **Loop Back** - Retry if needed (→2)

## API Endpoints

- `POST /query` - Process a single query
- `POST /batch` - Process multiple queries
- `GET /status` - Check system status
- `GET /history` - View query history

## Testing

```bash
poetry run pytest
```

For more details, see the documentation in the project root.