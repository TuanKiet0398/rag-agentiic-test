"""Main Agentic RAG Agent with 12-step workflow using Pydantic AI"""

import os
from datetime import datetime
from textwrap import dedent
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from pydantic_ai import Agent, RunContext
from pydantic_ai.ag_ui import StateDeps
from ag_ui.core import EventType, StateSnapshotEvent
from pydantic_ai.models.openai import OpenAIResponsesModel
from dotenv import load_dotenv

from .models import (
    QueryRewriteResult, SourceSelectionResult, RetrievalResult,
    ContextCompilationResult, GradingResult, FinalResponse, 
    WorkflowState, RAGAgentState
)
from .tools import (
    RAGDeps, retriever_tool, websearch_tool, api_tool, 
    enhance_query_tool, determine_api_type, lightrag_insert_tool,
    lightrag_batch_insert_tool, lightrag_status_tool, rag_query_tool
)

# Load environment variables
load_dotenv()


# =====
# Agent Configuration
# =====
class AgenticRAGProcessor:
    """Main processor for the 12-step Agentic RAG workflow"""
    
    def __init__(self):
        self.max_retries = int(os.getenv("MAX_RETRIES", "2"))
        self.acceptance_threshold = float(os.getenv("ACCEPTANCE_THRESHOLD", "0.7"))
        self.temperature = float(os.getenv("TEMPERATURE", "0.3"))
        self.max_tokens = int(os.getenv("MAX_TOKENS", "500"))
        
        # Initialize specialized agents for different steps
        self._setup_agents()
    
    def _setup_agents(self):
        """Setup specialized agents for different workflow steps"""
        
        # Step 1: Query Rewriting Agent
        self.query_rewriter = Agent(
            model=OpenAIResponsesModel('gpt-4o-mini'),
            deps_type=RAGDeps,
            result_type=QueryRewriteResult,
            system_prompt=dedent("""
                You are a query rewriting assistant. Your task is to analyze and improve user queries.

                Please:
                1. Identify the core intent of the question
                2. Clarify any ambiguous terms
                3. Expand abbreviations if needed
                4. Make the query more specific and searchable

                Rewrite the query to be more effective for retrieval systems.

                Return a JSON object with:
                - original_query: the input query
                - rewritten_query: your improved version
                - reasoning: explanation of changes made
            """).strip()
        )
        
        # Step 3: Source Selection Agent
        self.source_selector = Agent(
            model=OpenAIResponsesModel('gpt-4o-mini'),
            deps_type=RAGDeps,
            result_type=SourceSelectionResult,
            system_prompt=dedent("""
                You are a source selection assistant. Analyze the query and determine which data sources are needed.

                Evaluate:
                1. Is this a factual question that likely exists in documents?
                2. Does it require current/recent information?
                3. Does it need multiple perspectives?
                4. Is it a specialized domain question?

                Decide which sources to use:
                - vector_database: For stored knowledge, historical facts, domain-specific info
                - tools_apis: For real-time data, calculations, specific operations  
                - internet: For recent events, current news, trending topics

                Return a JSON object with:
                - primary_source: "vector_database" | "tools_apis" | "internet"
                - secondary_sources: array of additional sources
                - reasoning: explanation of decision
                - confidence: 0.0-1.0 confidence score
            """).strip()
        )
        
        # Step 7: Context Compilation Agent
        self.context_compiler = Agent(
            model=OpenAIResponsesModel('gpt-4o-mini'),
            deps_type=RAGDeps,
            result_type=ContextCompilationResult,
            system_prompt=dedent("""
                You are a context compilation assistant. Combine information from multiple sources.

                Tasks:
                1. Merge overlapping information
                2. Identify conflicting information and flag it
                3. Organize by relevance
                4. Remove redundancy

                Return a JSON object with:
                - compiled_context: combined and organized context
                - sources_used: array of sources
                - conflicts: array of any conflicting information
                - confidence: 0.0-1.0 confidence in compilation quality
            """).strip()
        )
        
        # Step 8-9: Response Generation Agent
        self.response_generator = Agent(
            model=OpenAIResponsesModel('gpt-4o-mini'),
            deps_type=RAGDeps,
            result_type=str,
            system_prompt=dedent("""
                You are an expert assistant providing accurate, concise answers based on provided context.

                INSTRUCTIONS:
                1. Answer directly and concisely
                2. Use ONLY information from the provided context
                3. If context is insufficient, acknowledge it
                4. Cite sources when possible
                5. Be factual and avoid speculation

                Generate your response based on the context and query provided.
            """).strip()
        )
        
        # Step 10: Self-Grading Agent
        self.grader = Agent(
            model=OpenAIResponsesModel('gpt-4o-mini'),
            deps_type=RAGDeps,
            result_type=GradingResult,
            system_prompt=dedent("""
                You are a quality assurance agent. Evaluate the generated response critically.

                Grade the response on these criteria (0.0 to 1.0):

                1. RELEVANCY: Does it directly answer the question?
                   - Consider: completeness, directness, clarity
                   
                2. FAITHFULNESS: Does it stay true to the context without hallucination?
                   - Check: no invented facts, no speculation beyond context
                   
                3. CONTEXT QUALITY: Was the retrieved context sufficient?
                   - Assess: completeness, relevance, currency

                4. COHERENCE: Is the response well-structured and clear?
                   - Evaluate: logical flow, readability

                Return a JSON object with:
                - relevancy_score: 0.0-1.0
                - faithfulness_score: 0.0-1.0  
                - context_quality_score: 0.0-1.0
                - coherence_score: 0.0-1.0
                - overall_score: 0.0-1.0 (average of above)
                - needs_improvement: true/false
                - improvement_reason: specific issues identified
                - recommendation: "retry_retrieval" | "web_search" | "accept" | "clarify_query"
            """).strip()
        )
    
    async def process_query_workflow(self, user_query: str, deps: RAGDeps) -> FinalResponse:
        """Execute the complete 12-step RAG workflow matching the exact diagram sequence"""
        
        # Initialize workflow state
        state = WorkflowState(
            original_query=user_query,
            max_retries=self.max_retries,
            acceptance_threshold=self.acceptance_threshold
        )
        
        try:
            # Execute the 12-step workflow matching the diagram
            while state.current_step <= 12 and state.retry_count <= state.max_retries:
                
                if state.current_step == 1:
                    # STEP 1: START - Initial Query (from diagram)
                    print(f"\n🎯 STEP 1: START")
                    print(f"   📝 Query: {state.original_query}")
                    state.current_step = 2
                
                elif state.current_step == 2:
                    # STEP 2: LLM Agent - Rewrite the initial query (from diagram)
                    print(f"\n🤖 STEP 2: LLM Agent - Rewrite the initial query")
                    result = await self.query_rewriter.run(
                        f"Original Query: {state.original_query}\n\nRewrite and improve this query for better retrieval.",
                        deps=deps
                    )
                    state.rewrite_result = result.data
                    print(f"   ✏️ Rewritten: {state.rewrite_result.rewritten_query}")
                    state.current_step = 3
                
                elif state.current_step == 3:
                    # STEP 3: Updated Query (from diagram)
                    print(f"\n📝 STEP 3: Updated query")
                    print(f"   📋 Query: {state.rewrite_result.rewritten_query}")
                    state.current_step = 4
                
                elif state.current_step == 4:
                    # STEP 4: LLM Agent - Do I need more details? (from diagram)
                    print(f"\n� STEP 4: LLM Agent - Do I need more details?")
                    details_check = await self.query_rewriter.run(
                        f"Query: {state.rewrite_result.rewritten_query}\n\nDoes this query need more details or clarification to be answered properly? Respond with YES or NO and explain briefly.",
                        deps=deps
                    )
                    
                    need_details = "yes" in details_check.data.rewritten_query.lower()
                    
                    if need_details:
                        print(f"   ✅ YES - Need more details, proceeding to source selection")
                        state.current_step = 5  # YES - Go to source selection
                    else:
                        # NO - Skip to step 12 (loop back as shown in diagram)
                        print(f"   ❌ NO - Query is clear enough, going to step 12")
                        state.current_step = 12
                
                elif state.current_step == 5:
                    # STEP 5: LLM Agent - Which source will help? (from diagram)
                    print(f"\n🤖 STEP 5: LLM Agent - Which source will help?")
                    result = await self.source_selector.run(
                        f"Query: {state.rewrite_result.rewritten_query}\n\nDetermine which data sources are needed for this query.",
                        deps=deps
                    )
                    state.source_selection_result = result.data
                    print(f"   🎯 Selected source: {state.source_selection_result.primary_source}")
                    state.current_step = 6
                
                elif state.current_step == 6:
                    # STEP 6: Source Selection & Retrieval (from diagram - Vector Database, Tools & APIs, Internet)
                    print(f"\n📚 STEP 6: Retrieving from sources")
                    updated_query = state.rewrite_result.rewritten_query
                    primary_source = state.source_selection_result.primary_source
                    
                    if primary_source == "vector_database":
                        print(f"   🗄️ Querying Vector Database")
                        result = await retriever_tool(RunContext(deps=deps), updated_query)
                    elif primary_source == "internet":
                        print(f"   🌐 Searching Internet")
                        result = await websearch_tool(RunContext(deps=deps), updated_query)
                    elif primary_source == "tools_apis":
                        print(f"   🔧 Calling Tools & APIs")
                        api_type = determine_api_type(updated_query)
                        result = await api_tool(RunContext(deps=deps), updated_query, api_type)
                    else:
                        print(f"   🗄️ Default: Querying Vector Database")
                        result = await retriever_tool(RunContext(deps=deps), updated_query)
                    
                    state.retrieval_result = result
                    print(f"   ✅ Retrieved {result.num_results} results")
                    state.current_step = 7
                
                elif state.current_step == 7:
                    # STEP 7: Retrieved Context (from diagram)
                    print(f"\n📄 STEP 7: Retrieved context")
                    vector_context = "\n".join(state.retrieval_result.documents) if state.retrieval_result.documents else ""
                    external_context = ""
                    
                    if state.retrieval_result.web_answer:
                        external_context += f"Web Search: {state.retrieval_result.web_answer}\n"
                    if state.retrieval_result.api_data:
                        external_context += f"API Data: {state.retrieval_result.api_data}\n"
                    
                    compilation_prompt = f"""Retrieved Context from Vector DB:
{vector_context}

Additional Context from Web/APIs:
{external_context}

Updated Query: {state.rewrite_result.rewritten_query}

Compile and organize this context."""
                    
                    result = await self.context_compiler.run(compilation_prompt, deps=deps)
                    state.context_result = result.data
                    print(f"   📋 Context compiled from {len(state.context_result.sources_used)} sources")
                    state.current_step = 8
                
                elif state.current_step == 8:
                    # STEP 8: Updated Query (from diagram - enhanced with retrieved context)
                    print(f"\n� STEP 8: Updated query")
                    # Enhance the query with retrieved context for better response generation
                    enhanced_query = f"Query: {state.rewrite_result.rewritten_query}\n\nAvailable Context: {state.context_result.compiled_context}"
                    state.enhanced_query = enhanced_query
                    print(f"   � Enhanced query prepared for response generation")
                    state.current_step = 9
                
                elif state.current_step == 9:
                    # STEP 9: LLM - Generate Response (from diagram)
                    print(f"\n🤖 STEP 9: LLM generating response")
                    response_prompt = f"""CONTEXT:
{state.context_result.compiled_context}

USER QUESTION:
{state.rewrite_result.rewritten_query}

Generate your response now."""
                    
                    result = await self.response_generator.run(response_prompt, deps=deps)
                    state.response = result.data
                    print(f"   💬 Response generated")
                    state.current_step = 10
                
                elif state.current_step == 10:
                    # STEP 10: LLM Agent - Is the answer relevant? (from diagram)
                    print(f"\n🤖 STEP 10: LLM Agent - Is the answer relevant?")
                    grading_prompt = f"""ORIGINAL QUERY: {state.rewrite_result.rewritten_query}
CONTEXT PROVIDED: {state.context_result.compiled_context}
GENERATED RESPONSE: {state.response}

Grade this response on the specified criteria."""
                    
                    result = await self.grader.run(grading_prompt, deps=deps)
                    state.grading_result = result.data
                    
                    # Check if answer is relevant (YES/NO decision from diagram)
                    if state.grading_result.overall_score >= state.acceptance_threshold:
                        print(f"   ✅ YES - Answer is relevant (score: {state.grading_result.overall_score:.2f})")
                        state.current_step = 11  # YES - Go to final response
                    else:
                        print(f"   ❌ NO - Answer needs improvement (score: {state.grading_result.overall_score:.2f})")
                        state.current_step = 12  # NO - Go to retry logic
                
                elif state.current_step == 11:
                    # STEP 11: Final Response (YES from Step 10)
                    print(f"\n🎉 STEP 11: Final response")
                    grading = state.grading_result
                    state.final_response = FinalResponse(
                        answer=state.response,
                        confidence=grading.overall_score,
                        sources=state.context_result.sources_used if state.context_result else [],
                        metadata={
                            "retrieval_method": state.retrieval_result.source if state.retrieval_result else "unknown",
                            "query_rewrites": state.retry_count + 1,
                            "grading_scores": grading,
                            "workflow_completed": True
                        }
                    )
                    print(f"   ✅ Workflow completed successfully!")
                    break
                
                elif state.current_step == 12:
                    # STEP 12: NO - Loop back to Step 2 (from diagram)
                    print(f"\n🔄 STEP 12: NO - Looping back to Step 2")
                    
                    if state.retry_count < state.max_retries:
                        state.retry_count += 1
                        grading = state.grading_result
                        
                        # Enhance query based on feedback before looping back to Step 2
                        if grading and grading.improvement_reason:
                            enhanced_query = await enhance_query_tool(
                                RunContext(deps=deps),
                                state.original_query,
                                grading.improvement_reason
                            )
                            # Update original query for rewriting in Step 2
                            state.original_query = enhanced_query
                            print(f"   📝 Enhanced query based on feedback")
                        
                        print(f"   ↩️ Retry {state.retry_count}/{state.max_retries} - Going back to Step 2")
                        state.current_step = 2  # Loop back to Step 2 as shown in diagram
                    
                    else:
                        # Max retries reached - use best available response
                        print(f"\n⚠️ STEP 12: Max retries reached, using best available response")
                        grading = state.grading_result if state.grading_result else None
                        state.final_response = FinalResponse(
                            answer=state.response + "\n\n[Note: Answer quality may be limited due to max retries reached]",
                            confidence=grading.overall_score if grading else 0.5,
                            sources=state.context_result.sources_used if state.context_result else [],
                            metadata={
                                "retrieval_method": state.retrieval_result.source if state.retrieval_result else "unknown",
                                "query_rewrites": state.retry_count,
                                "grading_scores": grading,
                                "note": "max_retries_reached",
                                "workflow_completed": False
                            }
                        )
                        break
            
            return state.final_response or FinalResponse(
                answer="Unable to generate satisfactory response",
                confidence=0.0,
                sources=[],
                metadata={"error": "workflow_incomplete"}
            )
            
        except Exception as e:
            return FinalResponse(
                answer=f"Error in RAG workflow: {str(e)}",
                confidence=0.0,
                sources=[],
                metadata={"error": str(e)}
            )


# Initialize the RAG processor
rag_processor = AgenticRAGProcessor()


# =====
# Main Agent
# =====
agent = Agent(
    model=OpenAIResponsesModel('gpt-4o-mini'),
    deps_type=StateDeps[RAGAgentState],
    system_prompt=dedent("""
        You are an advanced Agentic RAG assistant that processes queries through a sophisticated 12-step workflow:
        
        1. Query Rewrite - Optimize and clarify queries
        2. Source Selection - Choose best data sources  
        3. Retrieval - Get relevant information from LightRAG knowledge base
        4. Context Compilation - Organize retrieved data
        5. Response Generation - Create comprehensive answers
        6. Quality Validation - Self-grade and improve
        
        You have access to:
        - LightRAG knowledge base for document processing and advanced retrieval
        - Web search for current information  
        - APIs for real-time data
        - Quality control with retry mechanisms
        - Document indexing capabilities for expanding the knowledge base
        
        Key tools available:
        - agentic_rag_query: Process queries through the complete 12-step workflow
        - add_document_to_knowledge_base: Index new documents for future queries
        - batch_add_documents: Add multiple documents efficiently
        - check_knowledge_base_status: Monitor LightRAG system health
        
        Always use the agentic_rag_query tool for user questions. Use document tools when users want to add knowledge.
        Provide detailed, accurate responses with proper source attribution and confidence scoring.
    """).strip()
)

# =====
# Tools
# =====
@agent.tool
async def agentic_rag_query(
    ctx: RunContext[StateDeps[RAGAgentState]], 
    user_query: str
) -> StateSnapshotEvent:
    """
    Process a user query through the complete 12-step Agentic RAG workflow.
    
    This tool implements:
    - Query rewriting and optimization
    - Intelligent source selection
    - Multi-source retrieval (vector DB, web, APIs)
    - Context compilation and organization
    - Response generation with quality validation
    - Self-grading and retry loops for quality assurance
    """
    print(f"🔍 Processing RAG query: {user_query}")
    
    # Initialize RAG dependencies
    rag_deps = RAGDeps()
    
    # Process query through 12-step workflow
    final_response = await rag_processor.process_query_workflow(user_query, rag_deps)
    
    # Update agent state
    ctx.deps.state.query_history.append(user_query)
    ctx.deps.state.response_history.append(final_response)
    
    # Store current workflow state for debugging/analysis
    if rag_processor:
        workflow_state = WorkflowState(original_query=user_query)
        ctx.deps.state.current_workflow = workflow_state
    
    print(f"✅ RAG query completed with confidence: {final_response.confidence}")
    
    return StateSnapshotEvent(
        type=EventType.STATE_SNAPSHOT,
        snapshot=ctx.deps.state,
    )


@agent.tool  
def get_query_history(ctx: RunContext[StateDeps[RAGAgentState]]) -> list[str]:
    """Get the history of processed queries."""
    return ctx.deps.state.query_history


@agent.tool
def get_response_history(ctx: RunContext[StateDeps[RAGAgentState]]) -> list[FinalResponse]:
    """Get the history of RAG responses with metadata."""
    return ctx.deps.state.response_history


@agent.tool
def clear_history(ctx: RunContext[StateDeps[RAGAgentState]]) -> StateSnapshotEvent:
    """Clear the query and response history."""
    ctx.deps.state.query_history.clear()
    ctx.deps.state.response_history.clear()
    ctx.deps.state.current_workflow = None
    
    return StateSnapshotEvent(
        type=EventType.STATE_SNAPSHOT,
        snapshot=ctx.deps.state,
    )


@agent.tool
async def enhanced_rag_query(
    ctx: RunContext[StateDeps[RAGAgentState]], 
    query: str,
    mode: str = "hybrid"
) -> StateSnapshotEvent:
    """
    Enhanced RAG query tool using reference code patterns with Pydantic AI.
    
    This tool provides direct access to the LightRAG service using the improved
    query_rag_api function with comprehensive error handling and response processing.
    
    Args:
        query: The question or query to search for
        mode: LightRAG query mode - "local", "global", or "hybrid" (default)
    
    Returns:
        StateSnapshotEvent with processed results and updated state
    """
    print(f"🔍 Enhanced RAG query: {query} (mode: {mode})")
    
    # Initialize RAG dependencies
    rag_deps = RAGDeps()
    
    # Use the enhanced rag_query_tool with reference code patterns
    result = await rag_query_tool(RunContext(deps=rag_deps), query, mode)
    
    # Process the result and create a response
    if result.num_results > 0 and result.documents:
        content = result.documents[0]
        confidence = 0.8  # Default confidence for enhanced queries
        
        response = FinalResponse(
            content=content,
            confidence=confidence,
            sources=[f"LightRAG ({mode} mode)"],
            metadata={
                "mode": mode,
                "query": query,
                "tool": "enhanced_rag_query",
                "timestamp": datetime.now().isoformat()
            }
        )
    else:
        response = FinalResponse(
            content=f"No relevant information found for: {query}",
            confidence=0.1,
            sources=["LightRAG (no results)"],
            metadata={
                "mode": mode,
                "query": query,
                "tool": "enhanced_rag_query",
                "error": "No results found",
                "timestamp": datetime.now().isoformat()
            }
        )
    
    # Update agent state
    ctx.deps.state.query_history.append(query)
    ctx.deps.state.response_history.append(response)
    
    print(f"✅ Enhanced RAG query completed (confidence: {response.confidence})")
    
    return StateSnapshotEvent(
        type=EventType.STATE_SNAPSHOT,
        snapshot=ctx.deps.state,
    )


@agent.tool
async def add_document_to_knowledge_base(
    ctx: RunContext[StateDeps[RAGAgentState]], 
    text: str,
    title: Optional[str] = None,
    source: Optional[str] = None
) -> StateSnapshotEvent:
    """
    Add a new document to the LightRAG knowledge base for future queries.
    
    This tool enables dynamic knowledge base expansion by indexing new documents.
    """
    print(f"📄 Adding document to knowledge base: {title or 'Untitled'}")
    
    # Initialize RAG dependencies
    rag_deps = RAGDeps()
    
    # Prepare metadata
    metadata = {}
    if title:
        metadata["title"] = title
    if source:
        metadata["source"] = source
    metadata["added_at"] = datetime.now().isoformat()
    
    # Insert document into LightRAG
    result = await lightrag_insert_tool(RunContext(deps=rag_deps), text, metadata)
    
    if result.get("success"):
        print(f"✅ Document indexed successfully: {result.get('message')}")
        # Update agent state to reflect the addition
        if not hasattr(ctx.deps.state, 'documents_added'):
            ctx.deps.state.documents_added = 0
        ctx.deps.state.documents_added += 1
    else:
        print(f"❌ Failed to index document: {result.get('error')}")
    
    return StateSnapshotEvent(
        type=EventType.STATE_SNAPSHOT,
        snapshot=ctx.deps.state,
    )


@agent.tool
async def batch_add_documents(
    ctx: RunContext[StateDeps[RAGAgentState]], 
    documents: list[Dict[str, str]]
) -> StateSnapshotEvent:
    """
    Batch add multiple documents to the knowledge base.
    
    Each document should have 'text' and optionally 'title', 'source' fields.
    """
    print(f"📚 Batch adding {len(documents)} documents to knowledge base")
    
    # Initialize RAG dependencies  
    rag_deps = RAGDeps()
    
    # Add metadata to documents
    processed_docs = []
    for doc in documents:
        processed_doc = {
            "text": doc.get("text", ""),
            "metadata": {
                "title": doc.get("title", ""),
                "source": doc.get("source", ""),
                "added_at": datetime.now().isoformat()
            }
        }
        processed_docs.append(processed_doc)
    
    # Batch insert into LightRAG
    result = await lightrag_batch_insert_tool(RunContext(deps=rag_deps), processed_docs)
    
    if result.get("success"):
        print(f"✅ Batch indexing completed: {result.get('message')}")
        # Update agent state
        if not hasattr(ctx.deps.state, 'documents_added'):
            ctx.deps.state.documents_added = 0
        ctx.deps.state.documents_added += len(documents)
    else:
        print(f"❌ Batch indexing failed: {result.get('error')}")
    
    return StateSnapshotEvent(
        type=EventType.STATE_SNAPSHOT,
        snapshot=ctx.deps.state,
    )


@agent.tool
async def check_knowledge_base_status(ctx: RunContext[StateDeps[RAGAgentState]]) -> str:
    """
    Check the status and statistics of the LightRAG knowledge base.
    """
    print("🔍 Checking LightRAG knowledge base status")
    
    # Initialize RAG dependencies
    rag_deps = RAGDeps()
    
    # Get status from LightRAG
    status = await lightrag_status_tool(RunContext(deps=rag_deps))
    
    if status.get("available"):
        kb_stats = status.get("knowledge_base_stats", {})
        return f"""
LightRAG Knowledge Base Status:
✅ Status: Online and available
📊 Documents: {kb_stats.get('total_documents', 'N/A')}
🔗 Entities: {kb_stats.get('total_entities', 'N/A')}
🌐 Relationships: {kb_stats.get('total_relationships', 'N/A')}
🕒 Last Updated: {status.get('last_updated', 'Unknown')}
        """.strip()
    else:
        return f"❌ LightRAG Knowledge Base Status: {status.get('error', 'Unavailable')}"
