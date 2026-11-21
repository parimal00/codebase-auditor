from src.analysis.finding_prioritizer import FindingPrioritizer
from src.schemas.state import AuditState

def finding_prioritizer_node(state: AuditState) -> dict:
    """Sorts findings by severity."""
    print("🎯 Prioritizing audit findings...")

    prioritizer = FindingPrioritizer()

    findings = prioritizer.prioritize(
        state.get("findings", [])
    )

    return {
        "current_node": "finding_prioritizer",
        "findings": findings,
    }