from src.schemas.state import AuditState
from src.analysis.finding_deduplicator import FindingDeduplicator

def finding_deduplicator_node(state: AuditState) -> dict:
    print("🧹 Removing duplicate findings...")

    deduplicator = FindingDeduplicator()

    findings = deduplicator.deduplicate(
        state.get("findings", [])
    )

    return {
        "current_node": "finding_deduplicator",
        "findings": findings,
    }