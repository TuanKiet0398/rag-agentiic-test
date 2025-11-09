// State of the agent, make sure this aligns with your agent's state.
export type AgentState = {
  query_history: string[];
  response_history: FinalResponse[];
  current_workflow?: WorkflowState;
  documents_added?: number;
  lightrag_status?: string;
}

export type FinalResponse = {
  answer: string;
  confidence: number;
  sources: string[];
  metadata: Record<string, any>;
  query_rewrites?: number;
  grading_scores?: GradingResult;
}

export type GradingResult = {
  relevancy_score: number;
  faithfulness_score: number;
  context_quality_score: number;
  coherence_score: number;
  overall_score: number;
  needs_improvement: boolean;
  improvement_reason: string;
  recommendation: "retry_retrieval" | "web_search" | "accept" | "clarify_query";
}

export type WorkflowState = {
  original_query: string;
  current_step: number;
  retry_count: number;
  max_retries: number;
  acceptance_threshold: number;
}