from langchain_core.messages import HumanMessage
from rich import print

from src.schemas.state import AuditState
from src.config.llm import get_llm
from src.schemas.findings import AgentFindingReport
from src.analysis.context_builders import SecurityContextBuilder


def security_auditor_node(state: AuditState) -> dict:
    print("🔒 Running Security & Compliance Auditor...")

    parsed_ast = state.get("parsed_ast", [])
    context_builder = SecurityContextBuilder()
    sec_context = context_builder.build(parsed_ast)

    llm = get_llm()
    structured_llm = llm.with_structured_output(AgentFindingReport)

    prompt = f"""
    You are an expert Application Security Engineer. Analyze the following Python codebase metadata 
    for security vulnerabilities, hardcoded credentials, unsafe eval/exec usage, or injection risks:
    
    {sec_context.model_dump()}
    
    Return a list of findings matching the requested schema.
    """

    try:
        result: AgentFindingReport = structured_llm.invoke([HumanMessage(content=prompt)])
        findings = [f.model_dump() for f in result.findings]
    except Exception as e:
        print(f"[bold red]Error in Security Auditor:[/bold red] {e}")
        findings = []

    return {
        "security_findings": findings,
    }
