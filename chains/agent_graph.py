from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from agents.planner import PlannerAgent
from agents.responder import ResponderAgent
from agents.scheduler import SchedulerAgent
from agents.coder import CoderAgent
from agents.memory_agent import MemoryAgent

class AgentState(TypedDict):
    query: str
    context: List[str]
    next_agent: str
    response: str
    agents_used: List[str]

planner = PlannerAgent()
responder = ResponderAgent()
scheduler = SchedulerAgent()
coder = CoderAgent()
memory = MemoryAgent()

def plan_node(state: AgentState) -> AgentState:
    plan = planner.plan(state["query"])
    return {
        **state,
        "next_agent": plan["next_agent"],
        "context": plan["context"],
        "agents_used": ["Planner"]
    }

def agent_node(state: AgentState) -> AgentState:
    query, context, next_agent = state["query"], state["context"], state["next_agent"]
    if next_agent == "responder":
        response = responder.run(query, context)
    elif next_agent == "scheduler":
        response = scheduler.run(query, context)
    elif next_agent == "coder":
        response = coder.run(query, context)
    else:
        response = "❌ Invalid agent."
    state["response"] = response
    state["agents_used"].append(next_agent.capitalize())
    return state

def memory_node(state: AgentState) -> AgentState:
    memory.store_interaction(state["query"], state["response"], state["agents_used"])
    return state

def build_agent_graph():
    workflow = StateGraph(AgentState)
    workflow.add_node("plan", plan_node)
    workflow.add_node("dispatch", agent_node)
    workflow.add_node("memory", memory_node)
    workflow.set_entry_point("plan")
    workflow.add_edge("plan", "dispatch")
    workflow.add_edge("dispatch", "memory")
    workflow.add_edge("memory", END)
    return workflow.compile()
