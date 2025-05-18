from fastapi import FastAPI
from pydantic import BaseModel
from chains.agent_graph import build_agent_graph
from config import API_HOST, API_PORT
from memory.vectorstore import init_qdrant
import uvicorn

class AskRequest(BaseModel):
    query: str

class AskResponse(BaseModel):
    response: str
    agents_used: list[str]

app = FastAPI()
init_qdrant()
graph = build_agent_graph()

@app.post("/ask", response_model=AskResponse)
async def ask(request: AskRequest):
    try:
        state = graph.invoke({"query": request.query})
        return AskResponse(response=state["response"], agents_used=state["agents_used"])
    except Exception as e:
        return AskResponse(response=f"❌ Error: {str(e)}", agents_used=[])

if __name__ == "__main__":
    uvicorn.run("main:app", host=API_HOST, port=API_PORT, reload=True)
