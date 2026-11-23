from langchain_core.messages import HumanMessage

from src.config.llm import get_llm
from src.schemas.suggestions import ImprovementSuggestionReport
from src.schemas.state import AuditState


def improvement_suggestion_node(state: AuditState) -> dict:
    print("💡 Generating AI improvement suggestions...")

    findings = state.get("findings", [])

    if not findings:
        return {
            "current_node": "improvement_suggestion",
            "improvement_suggestions": [],
        }

    try:
        llm = get_llm()
        structured_llm = llm.with_structured_output(
            ImprovementSuggestionReport
        )

        prompt = f"""
        You are an experienced Senior Software Engineer.

        Analyze the following code audit findings and provide
        practical, actionable improvement suggestions.

        Findings:
        {findings}

        Instructions:
        - Provide one suggestion for each finding.
        - Preserve the original category, file_path, and title.
        - Focus on practical improvements.
        - Avoid generic advice.
        - Do not invent code details that are not present in the findings.
        - Do not repeat the original finding description.
        - Do not generate complete code implementations.

        Return suggestions matching the requested schema.
        """

        result: ImprovementSuggestionReport = structured_llm.invoke(
            [HumanMessage(content=prompt)]
        )

        suggestions = [
            suggestion.model_dump()
            for suggestion in result.suggestions
        ]

        return {
            "current_node": "improvement_suggestion",
            "improvement_suggestions": suggestions,
        }

    except Exception as e:
        print(f"[bold red]Error generating improvement suggestions:[/bold red] {e}")

        return {
            "current_node": "improvement_suggestion",
            "improvement_suggestions": [],
        }