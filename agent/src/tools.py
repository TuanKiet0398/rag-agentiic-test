"""Tools for the Agentic RAG System - Steps 6 retrieval operations with LightRAG integration"""

import os
import json
import logging
from datetime import datetime
from typing import Dict, List, Optional
import httpx
import requests
from pydantic_ai import RunContext

try:
    from tavily import TavilyClient
    TAVILY_AVAILABLE = True
except ImportError:
    TAVILY_AVAILABLE = False

from .models import RetrievalResult

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class RAGDeps:
    """Dependencies for RAG agent tools with LightRAG integration"""
    def __init__(self):
        self.lightrag_client = None
        self.tavily_client = None
        self.lightrag_base_url = os.getenv("LIGHT_RAG_HOST", "http://localhost:9621/query")
        self.lightrag_host_base = os.getenv("LIGHTRAG_URL", "http://localhost:9621") 
        self.setup_clients()
    
    def setup_clients(self):
        """Initialize external clients"""
        # Initialize LightRAG HTTP client (for async operations)
        try:
            self.lightrag_client = httpx.AsyncClient(
                base_url=self.lightrag_host_base,
                timeout=30.0
            )
            print(f"✅ LightRAG client initialized for {self.lightrag_host_base}")
        except Exception as e:
            print(f"Warning: Could not initialize LightRAG client: {e}")
        
        # Initialize Tavily client for web search
        if TAVILY_AVAILABLE:
            tavily_key = os.getenv("TAVILY_API_KEY")
            if tavily_key:
                try:
                    self.tavily_client = TavilyClient(api_key=tavily_key)
                    print("✅ Tavily client initialized")
                except Exception as e:
                    print(f"Warning: Could not initialize Tavily client: {e}")


async def retriever_tool(ctx: RunContext, question: str) -> RetrievalResult:
    """
    Retrieve relevant documents from LightRAG knowledge base.
    
    Uses the enhanced query_rag_api function with proper error handling
    following reference code patterns adapted for Pydantic AI.
    """
    try:
        # Determine the best query mode for LightRAG
        query_mode = determine_lightrag_mode(question)
        
        # Use the new query_rag_api function with proper error handling
        rag_result = query_rag_api(question, mode=query_mode)
        
        if rag_result.get("success", False):
            # Process successful response
            content = rag_result.get("content", "")
            
            if content:
                documents = [content]
                metadata = [{
                    "source": "lightrag_response",
                    "mode": query_mode,
                    "query": question,
                    "status_code": rag_result.get("status_code", 200)
                }]
            else:
                documents = ["No relevant documents found in LightRAG knowledge base"]
                metadata = [{"source": "lightrag_empty", "mode": query_mode}]
            
            return RetrievalResult(
                documents=documents,
                metadata=metadata,
                source="lightrag",
                num_results=len(documents)
            )
        
        else:
            # Handle error response from query_rag_api
            error_msg = rag_result.get("error", "Unknown LightRAG error")
            status_code = rag_result.get("status_code", "unknown")
            
            return RetrievalResult(
                documents=[f"LightRAG query failed: {error_msg}"],
                source="lightrag_error",
                num_results=0,
                metadata=[{
                    "error": error_msg,
                    "mode": query_mode,
                    "query": question,
                    "status_code": status_code
                }]
            )
        
    except Exception as e:
        return RetrievalResult(
            documents=[f"Error retrieving from LightRAG: {str(e)}"],
            source="lightrag_error", 
            num_results=0,
            metadata=[{
                "error": str(e),
                "query": question,
                "function": "retriever_tool"
            }]
        )


async def websearch_tool(ctx: RunContext, question: str) -> RetrievalResult:
    """
    Search the internet for current information using Tavily.
    """
    if not hasattr(ctx.deps, 'tavily_client') or not ctx.deps.tavily_client:
        return RetrievalResult(
            web_answer="Web search not available - Tavily client not configured",
            source="web_search_error",
            num_results=0
        )
    
    try:
        # Use Tavily's QnA search for direct answers
        answer = ctx.deps.tavily_client.qna_search(query=question)
        
        return RetrievalResult(
            web_answer=answer if answer else "No relevant information found on the web",
            source="internet",
            num_results=1 if answer else 0,
            timestamp=datetime.now()
        )
        
    except Exception as e:
        return RetrievalResult(
            web_answer=f"Error in web search: {str(e)}",
            source="web_search_error",
            num_results=0
        )


async def api_tool(ctx: RunContext, query: str, api_type: str) -> RetrievalResult:
    """
    Call external APIs for specific data.
    
    Supported APIs: weather, stock, calculation, etc.
    """
    try:
        if api_type == "weather":
            # Example weather API call (would need actual API key)
            api_data = {"weather": "sunny", "temperature": "72°F", "note": "Mock weather data - replace with real API"}
        
        elif api_type == "stock":
            # Example stock API call
            api_data = {"price": "$150.25", "change": "+2.5%", "note": "Mock stock data - replace with real API"}
        
        elif api_type == "calculation":
            # Simple calculation handling
            try:
                # Basic safe evaluation - in production, use a proper math parser
                clean_query = query.replace("calculate", "").strip()
                # Only allow basic math operations for safety
                allowed_chars = "0123456789+-*/.() "
                if all(c in allowed_chars for c in clean_query):
                    result = eval(clean_query)
                    api_data = {"calculation": query, "result": result}
                else:
                    api_data = {"error": "Invalid calculation - only basic math operations allowed"}
            except:
                api_data = {"error": "Invalid calculation"}
        
        else:
            api_data = {"error": f"API type '{api_type}' not supported"}
        
        return RetrievalResult(
            api_data=api_data,
            source=f"api_{api_type}",
            num_results=1
        )
        
    except Exception as e:
        return RetrievalResult(
            api_data={"error": f"API call failed: {str(e)}"},
            source=f"api_{api_type}_error",
            num_results=0
        )


async def enhance_query_tool(ctx: RunContext, original_query: str, issues: str) -> str:
    """
    Enhance query based on grading feedback for retry loops.
    """
    # Simple enhancement logic (in real implementation, this would use LLM)
    if "specific" in issues.lower():
        return f"Detailed information about: {original_query}"
    elif "context" in issues.lower() or "relevant" in issues.lower():
        return f"Comprehensive explanation of: {original_query}"
    elif "recent" in issues.lower() or "current" in issues.lower():
        return f"Current and up-to-date information about: {original_query}"
    elif "faithfulness" in issues.lower() or "hallucination" in issues.lower():
        return f"Factual and verified information about: {original_query}"
    else:
        return f"Complete guide to: {original_query}"


async def lightrag_insert_tool(ctx: RunContext, text: str, metadata: Optional[Dict] = None) -> Dict:
    """
    Insert/index new document into LightRAG knowledge base.
    
    This enables dynamic document processing and knowledge base expansion.
    """
    if not hasattr(ctx.deps, 'lightrag_client') or not ctx.deps.lightrag_client:
        return {"error": "LightRAG client not available", "success": False}
    
    try:
        # Prepare document data for LightRAG insertion
        doc_data = {
            "text": text,
            "metadata": metadata or {}
        }
        
        # Insert document using LightRAG's insert endpoint
        response = await ctx.deps.lightrag_client.post(
            "/insert",
            json=doc_data
        )
        
        if response.status_code == 200:
            result = response.json()
            return {
                "success": True,
                "message": "Document successfully indexed in LightRAG",
                "document_id": result.get("document_id"),
                "entities_extracted": result.get("entities", []),
                "relationships_created": result.get("relationships", 0)
            }
        else:
            return {
                "success": False,
                "error": f"LightRAG insertion failed: {response.status_code} - {response.text}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Error inserting document into LightRAG: {str(e)}"
        }


async def lightrag_batch_insert_tool(ctx: RunContext, documents: List[Dict]) -> Dict:
    """
    Batch insert multiple documents into LightRAG knowledge base.
    
    Efficient for processing multiple documents at once.
    """
    if not hasattr(ctx.deps, 'lightrag_client') or not ctx.deps.lightrag_client:
        return {"error": "LightRAG client not available", "success": False}
    
    try:
        # Prepare batch data
        batch_data = {
            "documents": documents
        }
        
        # Batch insert using LightRAG
        response = await ctx.deps.lightrag_client.post(
            "/batch_insert",
            json=batch_data
        )
        
        if response.status_code == 200:
            result = response.json()
            return {
                "success": True,
                "message": f"Successfully indexed {len(documents)} documents",
                "documents_processed": result.get("documents_processed", len(documents)),
                "total_entities": result.get("total_entities", 0),
                "total_relationships": result.get("total_relationships", 0)
            }
        else:
            return {
                "success": False,
                "error": f"LightRAG batch insertion failed: {response.status_code} - {response.text}"
            }
            
    except Exception as e:
        return {
            "success": False,
            "error": f"Error batch inserting documents: {str(e)}"
        }


async def lightrag_status_tool(ctx: RunContext) -> Dict:
    """
    Check LightRAG system status and knowledge base statistics.
    """
    if not hasattr(ctx.deps, 'lightrag_client') or not ctx.deps.lightrag_client:
        return {"error": "LightRAG client not available", "available": False}
    
    try:
        # Get system status
        response = await ctx.deps.lightrag_client.get("/status")
        
        if response.status_code == 200:
            status_data = response.json()
            return {
                "available": True,
                "status": "online",
                "knowledge_base_stats": status_data.get("kb_stats", {}),
                "server_info": status_data.get("server_info", {}),
                "last_updated": datetime.now().isoformat()
            }
        else:
            return {
                "available": False,
                "error": f"LightRAG status check failed: {response.status_code}"
            }
            
    except httpx.RequestError:
        return {
            "available": False,
            "error": f"LightRAG not reachable at {ctx.deps.lightrag_base_url}"
        }
    except Exception as e:
        return {
            "available": False,
            "error": f"Error checking LightRAG status: {str(e)}"
        }


def determine_api_type(query: str) -> str:
    """Determine API type based on query content"""
    query_lower = query.lower()
    
    if any(word in query_lower for word in ["weather", "temperature", "rain", "sunny", "cloudy", "forecast"]):
        return "weather"
    elif any(word in query_lower for word in ["stock", "price", "market", "trading", "shares"]):
        return "stock"  
    elif any(word in query_lower for word in ["calculate", "math", "compute", "+", "-", "*", "/", "equation"]):
        return "calculation"
    else:
        return "general"


def determine_lightrag_mode(query: str) -> str:
    """Determine the best LightRAG query mode based on query type"""
    query_lower = query.lower()
    
    # Use local mode for simple factual queries
    if any(word in query_lower for word in ["what is", "define", "definition", "meaning"]):
        return "local"
    
    # Use global mode for broad conceptual queries
    elif any(word in query_lower for word in ["compare", "relationship", "overview", "summary", "analyze"]):
        return "global"
    
    # Use hybrid mode for complex queries (default)
    else:
        return "hybrid"


def query_rag_api(query: str, mode: str = "hybrid") -> dict:
    """
    Query the RAG API with proper error handling and response processing
    Based on reference LangChain implementation but adapted for Pydantic AI
    """
    # Use the configured LightRAG endpoint
    lightrag_url = os.getenv("LIGHT_RAG_HOST", "http://localhost:9621/query")
    
    try:
        # Prepare the payload for LightRAG API
        payload = {
            "query": query,
            "mode": mode  # local, global, or hybrid
        }
        
        # Make the request to LightRAG service
        logger.info(f"Querying LightRAG API: {lightrag_url} with mode: {mode}")
        response = requests.post(
            lightrag_url,
            json=payload,
            timeout=30
        )
        
        # Check if the request was successful
        response.raise_for_status()
        
        # Parse the response
        result = response.json()
        
        # Log successful response
        logger.info(f"Successfully received response from LightRAG API")
        
        return {
            "success": True,
            "content": result.get("response", ""),
            "mode": mode,
            "query": query,
            "status_code": response.status_code
        }
        
    except requests.exceptions.Timeout:
        logger.error("Timeout while querying LightRAG API")
        return {
            "success": False,
            "error": "Request timeout while querying RAG API",
            "mode": mode,
            "query": query
        }
        
    except requests.exceptions.ConnectionError:
        logger.error(f"Connection error to LightRAG API at {lightrag_url}")
        return {
            "success": False,
            "error": f"Could not connect to RAG API at {lightrag_url}",
            "mode": mode,
            "query": query
        }
        
    except requests.exceptions.HTTPError as e:
        logger.error(f"HTTP error from LightRAG API: {e}")
        return {
            "success": False,
            "error": f"HTTP error from RAG API: {e}",
            "mode": mode,
            "query": query,
            "status_code": getattr(e.response, 'status_code', None)
        }
        
    except ValueError as e:
        logger.error(f"JSON decode error from LightRAG API: {e}")
        return {
            "success": False,
            "error": f"Invalid JSON response from RAG API: {e}",
            "mode": mode,
            "query": query
        }
        
    except Exception as e:
        logger.error(f"Unexpected error querying LightRAG API: {e}")
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "mode": mode,
            "query": query
        }


async def rag_query_tool(ctx: RunContext, query: str, mode: str = "hybrid") -> RetrievalResult:
    """
    Pydantic AI tool for querying LightRAG using the reference code patterns.
    
    This tool wraps the query_rag_api function to provide a proper Pydantic AI
    tool interface while maintaining the error handling and response processing
    from the reference LangChain implementation.
    
    Args:
        query: The question or query to search for
        mode: LightRAG query mode - "local", "global", or "hybrid" (default)
    
    Returns:
        RetrievalResult with processed content and metadata
    """
    try:
        # Use the query_rag_api function with reference code patterns
        rag_result = query_rag_api(query, mode=mode)
        
        if rag_result.get("success", False):
            # Process successful response
            content = rag_result.get("content", "")
            status_code = rag_result.get("status_code", 200)
            
            if content:
                return RetrievalResult(
                    documents=[content],
                    metadata=[{
                        "source": "lightrag_rag_tool",
                        "mode": mode,
                        "query": query,
                        "status_code": status_code,
                        "success": True
                    }],
                    source="lightrag",
                    num_results=1
                )
            else:
                return RetrievalResult(
                    documents=["No content returned from LightRAG"],
                    metadata=[{
                        "source": "lightrag_rag_tool_empty", 
                        "mode": mode,
                        "query": query,
                        "status_code": status_code
                    }],
                    source="lightrag",
                    num_results=0
                )
        
        else:
            # Handle error response
            error_msg = rag_result.get("error", "Unknown error")
            status_code = rag_result.get("status_code", "unknown")
            
            return RetrievalResult(
                documents=[f"LightRAG query failed: {error_msg}"],
                metadata=[{
                    "source": "lightrag_rag_tool_error",
                    "mode": mode,
                    "query": query,
                    "error": error_msg,
                    "status_code": status_code,
                    "success": False
                }],
                source="lightrag_error",
                num_results=0
            )
            
    except Exception as e:
        logger.error(f"Error in rag_query_tool: {e}")
        return RetrievalResult(
            documents=[f"Unexpected error in RAG query tool: {str(e)}"],
            metadata=[{
                "source": "lightrag_rag_tool_exception",
                "mode": mode,
                "query": query,
                "error": str(e),
                "success": False
            }],
            source="lightrag_error",
            num_results=0
        )