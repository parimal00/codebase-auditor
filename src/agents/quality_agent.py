from langchain_core.messages import HumanMessage
from rich import print

from src.schemas.state import AuditState
from src.config.llm import get_llm
from src.schemas.findings import AgentFindingReport
from src.analysis.context_builders import QualityContextBuilder
from src.analysis.quality_rules import ComplexityRule


def quality_auditor_node(state: AuditState) -> dict:
    print("🧹 Running Code Quality Auditor...")

    parsed_ast = state.get("parsed_ast", [])

    # 1. Deterministic complexity analysis
    complexity_rule = ComplexityRule()
    deterministic_findings = complexity_rule.analyze(parsed_ast)
    deterministic_findings_dicts = [f.model_dump() for f in deterministic_findings]

    # 2. Build quality context DTO
    context_builder = QualityContextBuilder()
    quality_context = context_builder.build(parsed_ast)

    # 3. LLM semantic analysis
    llm_findings_dicts = []
    try:
        llm = get_llm()
        structured_llm = llm.with_structured_output(AgentFindingReport)

        prompt = f"""
    You are an expert Code Quality Engineer. Analyze the following Python codebase quality metadata 
    for semantic quality issues such as code smells, missing docstrings, or poor naming conventions:
    
    {quality_context.model_dump()}
    
    Note: Do not calculate cyclomatic complexity, as that has already been evaluated deterministically.
    Return a list of findings matching the requested schema.
    """
        result: AgentFindingReport = structured_llm.invoke([HumanMessage(content=prompt)])
        llm_findings_dicts = [f.model_dump() for f in result.findings]
    except Exception as e:
        print(f"[bold red]Error in Quality Auditor:[/bold red] {e}")

    # 4. Merge deterministic and LLM findings (deterministic findings are always preserved)
    return {
        "quality_findings": deterministic_findings_dicts + llm_findings_dicts,
    }
