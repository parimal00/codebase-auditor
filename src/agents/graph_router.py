from langgraph.graph import StateGraph, END
from src.schemas.state import AuditState
from src.agents.architecture_agent import architecture_auditor_node
from src.agents.quality_agent import quality_auditor_node
from src.agents.security_agent import security_auditor_node
def build_audit_graph():
    workflow = StateGraph(AuditState)
    
    workflow.add_node("architecture", architecture_auditor_node)
    workflow.add_node("quality", quality_auditor_node)
    workflow.add_node("security", security_auditor_node)
    
    workflow.set_entry_point("architecture")
    workflow.add_edge("architecture", "quality")
    workflow.add_edge("quality", "security")
    workflow.add_edge("security", END)
    
    
    return workflow.compile()