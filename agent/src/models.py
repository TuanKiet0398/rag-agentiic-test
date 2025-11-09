"""Data models for the 12-step Agentic RAG System"""

from datetime import datetime
from typing import Dict, List, Optional, Union, Literal
from pydantic import BaseModel, Field


class QueryRewriteResult(BaseModel):
    """Result of query rewriting (Steps 1-2)"""
    original_query: str
    rewritten_query: str
    reasoning: str


class SourceSelectionResult(BaseModel):
    """Result of source selection (Step 3)"""
    primary_source: Literal["vector_database", "tools_apis", "internet"]
    secondary_sources: List[str] = []
    reasoning: str
    confidence: float = Field(ge=0.0, le=1.0)


class RetrievalResult(BaseModel):
    """Result of retrieval operations (Step 6)"""
    documents: List[str] = []
    metadata: List[Dict] = []
    web_answer: Optional[str] = None
    api_data: Optional[Dict] = None
    source: str
    num_results: int = 0
    timestamp: datetime = Field(default_factory=datetime.now)


class ContextCompilationResult(BaseModel):
    """Result of context compilation (Step 7)"""
    compiled_context: str
    sources_used: List[str]
    conflicts: List[str] = []
    confidence: float = Field(ge=0.0, le=1.0)


class GradingResult(BaseModel):
    """Result of self-grading validation (Step 10)"""
    relevancy_score: float = Field(ge=0.0, le=1.0)
    faithfulness_score: float = Field(ge=0.0, le=1.0)
    context_quality_score: float = Field(ge=0.0, le=1.0)
    coherence_score: float = Field(ge=0.0, le=1.0)
    overall_score: float = Field(ge=0.0, le=1.0)
    needs_improvement: bool
    improvement_reason: str = ""
    recommendation: Literal["retry_retrieval", "web_search", "accept", "clarify_query"] = "accept"


class FinalResponse(BaseModel):
    """Final response structure (Step 11)"""
    answer: str
    confidence: float = Field(ge=0.0, le=1.0)
    sources: List[str]
    metadata: Dict = Field(default_factory=dict)
    query_rewrites: int = 0
    grading_scores: Optional[GradingResult] = None


class WorkflowState(BaseModel):
    """State management for the 12-step workflow"""
    original_query: str
    current_step: int = 1
    retry_count: int = 0
    max_retries: int = 2
    acceptance_threshold: float = 0.7
    
    # Step results
    rewrite_result: Optional[QueryRewriteResult] = None
    source_selection_result: Optional[SourceSelectionResult] = None
    retrieval_result: Optional[RetrievalResult] = None
    context_result: Optional[ContextCompilationResult] = None
    response: Optional[str] = None
    grading_result: Optional[GradingResult] = None
    final_response: Optional[FinalResponse] = None


class RAGAgentState(BaseModel):
    """Main agent state for the Agentic RAG system"""
    current_workflow: Optional[WorkflowState] = None
    query_history: List[str] = Field(default_factory=list, description="History of processed queries")
    response_history: List[FinalResponse] = Field(default_factory=list, description="History of responses")
    documents_added: int = Field(default=0, description="Number of documents added to knowledge base")
    lightrag_status: Optional[str] = Field(default=None, description="Current LightRAG system status")