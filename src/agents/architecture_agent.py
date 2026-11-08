from langchain_core.messages import HumanMessage
from src.schemas.state import AuditState
from src.config.llm import get_llm
from src.schemas.findings import AgentFindingReport
def architecture_auditor_node(state: AuditState) -> AuditState:
    print("Running Architecture Auditor Node...")
    
    
    llm = get_llm()
    structured_llm = llm.with_structured_output(AgentFindingReport)
    
    parsed_ast = state.get("parsed_ast", [])
    
    prompt = f"""
    You are an expert Software Architect. Analyze the following Python codebase AST metadata 
    for architectural anti-patterns, circular dependencies, poor separation of concerns, or bad layering:
    
    {parsed_ast}
    
    Return a list of findings matching the requested schema.
    """

    try:
        result: AgentFindingReport = structured_llm.invoke([HumanMessage(content=prompt)])
        print(f"Raw Structured LLM Output: {result}")
        new_findings = [f.model_dump() for f in result.findings]
    except Exception as e:
        print(f"Error in Architecture Auditor: {e}")
        new_findings = []
        
    existing_findings = state.get("findings", [])
    
    return {
        "findings": existing_findings + new_findings,
        "current_node": "architecture_auditor",
    }