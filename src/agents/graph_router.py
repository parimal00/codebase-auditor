from langgraph.graph import StateGraph, END, START
from src.schemas.state import AuditState
from src.agents.architecture_agent import architecture_auditor_node
from src.agents.quality_agent import quality_auditor_node
from src.agents.security_agent import security_auditor_node
from src.agents.rag_search import rag_search_node
from src.agents.router import router_node

def aggregator_node(state: AuditState) -> AuditState:
    """Combines findings or finalizes state after parallel agent execution."""
    print("📊 Aggregating audit findings from all agents...")
    return {"current_node": "aggregator"}

def audit_node(state: AuditState) -> dict:
    """Entry point for parallel code auditing."""
    print("🔍 Starting parallel code audit...")
    return {"current_node": "audit_node"}

def off_topic_node(state: AuditState) -> dict:
    """Rejects off-topic prompts or small talk."""
    return {
        "rag_response": {"answer": "I can only assist with codebase queries and code audits.", "referenced_files": []}
    }

def route_next_step(state: AuditState) -> str:
    routes = {
        "rag_search": "rag_search",
        "code_audit": "audit_node",
    }

    return routes.get(state.get("route"), "off_topic")
    
def build_audit_graph():
    workflow = StateGraph(AuditState)
    
    workflow.add_node("router", router_node)
    workflow.add_node("rag_search", rag_search_node)
    workflow.add_node("architecture_auditor", architecture_auditor_node)
    workflow.add_node("off_topic", off_topic_node)
    workflow.add_node("audit_node", audit_node)

    workflow.add_node("quality_auditor", quality_auditor_node)
    workflow.add_node("security_auditor", security_auditor_node)
    workflow.add_node("aggregator", aggregator_node)

    workflow.add_edge(START, "router")
    
    workflow.add_conditional_edges(
        "router",
        route_next_step,
        {
            "rag_search": "rag_search",
            "code_audit": "audit_node",
            "off_topic": "off_topic"
        }
    )
    workflow.add_edge("audit_node", "quality_auditor")
    workflow.add_edge("audit_node", "security_auditor")
    workflow.add_edge("audit_node", "architecture_auditor")
    workflow.add_edge("quality_auditor", "aggregator")
    workflow.add_edge("security_auditor", "aggregator")
    workflow.add_edge("architecture_auditor", "aggregator")
    
    workflow.add_edge("rag_search", "aggregator")
    workflow.add_edge("off_topic", "aggregator")
    
    workflow.add_edge("aggregator", END)
    
    return workflow.compile()