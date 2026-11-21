from src.schemas.state import AuditState
from src.config.llm import get_llm
from src.schemas.findings import AgentFindingReport
from langchain_core.messages import HumanMessage
from rich import print

def quality_auditor_node(state: AuditState) -> AuditState:
    print("🧹 Running Code Quality Auditor...")
    
    llm = get_llm()
    structured_llm = llm.with_structured_output(AgentFindingReport)
    
    parsed_ast = state.get("parsed_ast", [])
    
    prompt = f"""
    You are an expert Code Quality Engineer. Analyze the following Python codebase metadata 
    for code smells, overly complex functions, missing docstrings, or poor naming conventions:
    
    {parsed_ast}
    
    Return a list of findings matching the requested schema.
    """

    try:
        result: AgentFindingReport = structured_llm.invoke([HumanMessage(content=prompt)])
        findings = [f.model_dump() for f in result.findings]
    except Exception as e:
        print(f"[bold red]Error in Quality Auditor:[/bold red] {e}")
        findings = []
            
    return {
        "quality_findings": findings,
    }

