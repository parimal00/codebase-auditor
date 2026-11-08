from langgraph.graph import StateGraph, END, START
from src.schemas.state import AuditState
from src.agents.architecture_agent import architecture_auditor_node
from src.agents.quality_agent import quality_auditor_node
from src.agents.security_agent import security_auditor_node

def aggregator_node(state: AuditState) -> AuditState:
    """Combines findings or finalizes state after parallel agent execution."""
    print("📊 Aggregating audit findings from all agents...")
    return {"current_node": "aggregator"}

def build_audit_graph():
    workflow = StateGraph(AuditState)
    
    workflow.add_node("architecture", architecture_auditor_node)
    workflow.add_node("quality", quality_auditor_node)
    workflow.add_node("security", security_auditor_node)
    workflow.add_node("aggregator", aggregator_node)
    
    workflow.add_edge(START, "architecture_auditor")
    workflow.add_edge(START, "quality_auditor")
    workflow.add_edge(START, "security_auditor")
    
    workflow.add_edge("architecture_auditor", "aggregator")
    workflow.add_edge("quality_auditor", "aggregator")
    workflow.add_edge("security_auditor", "aggregator")
    
    workflow.add_edge("aggregator", END)
    
    return workflow.compile()