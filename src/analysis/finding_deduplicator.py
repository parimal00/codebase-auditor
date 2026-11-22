class FindingDeduplicator:
    SEVERITY_ORDER = {
        "critical": 1,
        "high": 2,
        "medium": 3,
        "low": 4,
    }

    def deduplicate(self, findings: list[dict]) -> list[dict]:
        unique_findings = {}

        for finding in findings:
            key = (
                finding["category"],
                finding["file_path"],
                finding["title"],
            )

            existing = unique_findings.get(key)

            if existing is None:
                unique_findings[key] = finding
                continue

            current_severity = self.SEVERITY_ORDER.get(
                finding["severity"].lower(),
                5,
            )

            existing_severity = self.SEVERITY_ORDER.get(
                existing["severity"].lower(),
                5,
            )

            if current_severity < existing_severity:
                unique_findings[key] = finding

        return list(unique_findings.values())