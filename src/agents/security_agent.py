from src.schemas.state import AuditState
from src.config.llm import get_llm
from src.schemas.findings import AgentFindingReport
from langchain_core.messages import HumanMessage

def security_auditor_node(state: AuditState) -> AuditState:
    print("🔒 Running Security & Compliance Auditor...")
    
    llm = get_llm()
    structured_llm = llm.with_structured_output(AgentFindingReport)
    
    parsed_ast = state.get("parsed_ast", [])
    
    prompt = f"""
    You are an expert Application Security Engineer. Analyze the following Python codebase metadata 
    for security vulnerabilities, hardcoded credentials, unsafe eval/exec usage, or injection risks:
    
    {parsed_ast}
    
    Return a list of findings matching the requested schema.
    """

    try:
        result: AgentFindingReport = structured_llm.invoke([HumanMessage(content=prompt)])
        new_findings = [f.model_dump() for f in result.findings]
    except Exception as e:
        print(f"Error in Security Auditor: {e}")
        new_findings = []
        
    existing_findings = state.get("findings", [])
    
    return {
        "findings": existing_findings + new_findings,
        "current_node": "security_auditor"
    }