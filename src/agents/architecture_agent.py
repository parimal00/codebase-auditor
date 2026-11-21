from langchain_core.messages import HumanMessage
from rich import print

from src.schemas.state import AuditState
from src.config.llm import get_llm
from src.schemas.findings import AgentFindingReport
from src.analysis.context_builders import ArchitectureContextBuilder


def architecture_auditor_node(state: AuditState) -> dict:
    print("Running Architecture Auditor Node...")

    parsed_ast = state.get("parsed_ast", [])
    context_builder = ArchitectureContextBuilder()
    arch_context = context_builder.build(parsed_ast)

    llm = get_llm()
    structured_llm = llm.with_structured_output(AgentFindingReport)

    prompt = f"""
    You are an expert Software Architect. Analyze the following Python codebase AST metadata 
    for architectural anti-patterns, circular dependencies, poor separation of concerns, or bad layering:
    
    {arch_context.model_dump()}
    
    Return a list of findings matching the requested schema.
    """

    try:
        result: AgentFindingReport = structured_llm.invoke([HumanMessage(content=prompt)])
        print(f"Raw Structured LLM Output: {result}")
        findings = [f.model_dump() for f in result.findings]
    except Exception as e:
        print(f"[bold red]Error in Architecture Auditor:[/bold red] {e}")
        findings = []

    return {
        "architecture_findings": findings,
    }
