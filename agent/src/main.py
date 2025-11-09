
from agent import agent, StateDeps
from models import RAGAgentState

app = agent.to_ag_ui(deps=StateDeps(RAGAgentState()))

if __name__ == "__main__":
    # run the app
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
