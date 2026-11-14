from src.schemas.state import AuditState
from src.config.llm import get_llm
from langchain_core.messages import HumanMessage
from src.schemas.route_decision import RouteDecision

def router_node(state: AuditState) -> dict:
    """Classifies user query intent for conditional graph routing."""
    user_query = state.get("user_query", "")
    
    llm = get_llm()
    structured_llm = llm.with_structured_output(RouteDecision)
    
    prompt = f"""
    You are a strict codebase assistant guardrail. Determine the intent of this input: "{user_query}"
    - 'rag_search': Asking how a specific feature, module, or code logic works.
    - 'code_audit': Asking to run quality, security, or structural code reviews.
    - 'off_topic': Small talk, greetings ("how are you"), or non-technical queries.
    """
    
    decision: RouteDecision = structured_llm.invoke([HumanMessage(content=prompt)])
    
    return {
        "route": decision.intent,
        "router_reasoning": decision.reasoning
    }