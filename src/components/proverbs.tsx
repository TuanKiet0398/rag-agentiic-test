import { AgentState, FinalResponse } from "@/lib/types";

export interface RAGCardProps {
  state: AgentState;
  setState: (state: AgentState) => void;
}

function getConfidenceClass(confidence: number): string {
  if (confidence >= 0.8) return 'high';
  if (confidence >= 0.6) return 'medium';
  return 'low';
}

function getConfidenceColor(confidence: number): string {
  if (confidence >= 0.8) return 'bg-green-500';
  if (confidence >= 0.6) return 'bg-yellow-500';
  return 'bg-red-500';
}

export function ProverbsCard({ state, setState }: RAGCardProps) {
  return (
    <div className="bg-white/20 backdrop-blur-md p-8 rounded-2xl shadow-xl max-w-4xl w-full">
      <h1 className="text-4xl font-bold text-white mb-2 text-center">Agentic RAG System</h1>
      <p className="text-gray-200 text-center italic mb-6">
        12-Step Intelligent Query Processing with Pydantic AI 🤖
      </p>
      
      <div className="bg-white/10 p-4 rounded-xl mb-6">
        <h3 className="text-white font-semibold mb-2">RAG Workflow Features:</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-2 text-sm text-gray-200">
          <div>• Query rewriting & optimization</div>
          <div>• Intelligent source selection</div>
          <div>• LightRAG knowledge base retrieval</div>
          <div>• Web search integration</div>
          <div>• Context compilation</div>
          <div>• Self-grading validation</div>
          <div>• Quality control loops</div>
          <div>• Dynamic document indexing</div>
        </div>
        
        {/* LightRAG Status */}
        <div className="mt-4 pt-3 border-t border-white/20">
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-300">Knowledge Base:</span>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 rounded-full bg-green-400"></div>
              <span className="text-green-200">LightRAG Connected</span>
            </div>
          </div>
          
          {state.documents_added !== undefined && state.documents_added > 0 && (
            <div className="mt-2 text-xs text-blue-200">
              📄 Documents indexed: {state.documents_added}
            </div>
          )}
        </div>
      </div>
      
      <hr className="border-white/20 my-6" />
      
      {/* Query History */}
      {state.query_history && state.query_history.length > 0 && (
        <div className="mb-6">
          <h3 className="text-white font-semibold mb-3">Recent Queries:</h3>
          <div className="flex flex-col gap-2">
            {state.query_history.slice(-3).map((query, index) => (
              <div 
                key={index} 
                className="bg-white/10 p-3 rounded-lg text-white text-sm"
              >
                "{query}"
              </div>
            ))}
          </div>
        </div>
      )}
      
      {/* Response History */}
      <div className="flex flex-col gap-4">
        {state.response_history && state.response_history.length > 0 ? (
          state.response_history.slice(-2).map((response: FinalResponse, index) => (
            <div 
              key={index} 
              className="bg-white/15 p-6 rounded-xl text-white relative group hover:bg-white/20 transition-all"
            >
              {/* Answer */}
              <div className="mb-4">
                <h4 className="font-semibold text-blue-200 mb-2">Response:</h4>
                <p className="text-white leading-relaxed">{response.answer}</p>
              </div>
              
              {/* Confidence & Metadata */}
              <div className="flex flex-wrap items-center gap-4 mb-3">
                <div className="flex items-center gap-2">
                  <span className="text-gray-300 text-sm">Confidence:</span>
                  <div className={`px-2 py-1 rounded text-white text-xs font-bold ${getConfidenceColor(response.confidence)}`}>
                    {(response.confidence * 100).toFixed(1)}%
                  </div>
                </div>
                
                {response.metadata?.retrieval_method && (
                  <div className="text-gray-300 text-xs">
                    Method: {response.metadata.retrieval_method}
                  </div>
                )}
                
                {response.metadata?.query_rewrites !== undefined && (
                  <div className="text-gray-300 text-xs">
                    Rewrites: {response.metadata.query_rewrites}
                  </div>
                )}
              </div>
              
              {/* Quality Scores */}
              {response.grading_scores && (
                <div className="mb-3">
                  <div className="text-gray-300 text-xs mb-2">Quality Scores:</div>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-2">
                    <div className="bg-white/10 p-2 rounded text-center">
                      <div className="text-xs text-gray-300">Relevancy</div>
                      <div className="text-white font-semibold">{(response.grading_scores.relevancy_score * 100).toFixed(0)}%</div>
                    </div>
                    <div className="bg-white/10 p-2 rounded text-center">
                      <div className="text-xs text-gray-300">Faithfulness</div>
                      <div className="text-white font-semibold">{(response.grading_scores.faithfulness_score * 100).toFixed(0)}%</div>
                    </div>
                    <div className="bg-white/10 p-2 rounded text-center">
                      <div className="text-xs text-gray-300">Context</div>
                      <div className="text-white font-semibold">{(response.grading_scores.context_quality_score * 100).toFixed(0)}%</div>
                    </div>
                    <div className="bg-white/10 p-2 rounded text-center">
                      <div className="text-xs text-gray-300">Coherence</div>
                      <div className="text-white font-semibold">{(response.grading_scores.coherence_score * 100).toFixed(0)}%</div>
                    </div>
                  </div>
                </div>
              )}
              
              {/* Sources */}
              {response.sources && response.sources.length > 0 && (
                <div className="mb-3">
                  <div className="text-gray-300 text-xs mb-2">Sources:</div>
                  <div className="flex flex-wrap gap-1">
                    {response.sources.map((source, i) => (
                      <span key={i} className="bg-blue-500/30 text-blue-200 px-2 py-1 rounded text-xs">
                        {source}
                      </span>
                    ))}
                  </div>
                </div>
              )}
              
              <button 
                onClick={() => {
                  const newHistory = state.response_history?.filter((_, i) => i !== index) || [];
                  setState({
                    ...state,
                    response_history: newHistory,
                  });
                }}
                className="absolute right-3 top-3 opacity-0 group-hover:opacity-100 transition-opacity 
                  bg-red-500 hover:bg-red-600 text-white rounded-full h-6 w-6 flex items-center justify-center"
              >
                ✕
              </button>
            </div>
          ))
        ) : (
          <p className="text-center text-white/80 italic py-8">
            No RAG responses yet. Ask the assistant any question to see the 12-step workflow in action!
          </p>
        )}
      </div>
      
      {/* Clear History Button */}
      {(state.query_history?.length > 0 || state.response_history?.length > 0) && (
        <div className="text-center mt-6">
          <button
            onClick={() => setState({
              ...state,
              query_history: [],
              response_history: [],
              current_workflow: undefined
            })}
            className="bg-white/20 hover:bg-white/30 text-white px-4 py-2 rounded-lg transition-all text-sm"
          >
            Clear History
          </button>
        </div>
      )}
    </div>
  );
}