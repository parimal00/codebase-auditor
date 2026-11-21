class FindingPrioritizer:
    SEVERITY_ORDER = {
        "critical": 1,
        "high": 2,
        "medium": 3,
        "low": 4,
    }

    def prioritize(self, findings):
        return sorted(
            findings,
            key=lambda finding: self.SEVERITY_ORDER.get(
                finding["severity"].lower(),
                5,
            ),
        )