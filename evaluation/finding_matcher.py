
class FindingMatcher:
    ISSUE_KEYWORDS = {
        "high_cyclomatic_complexity": [
            "complexity",
            "cyclomatic",
        ],
        "missing_docstring": [
            "docstring",
        ],
        "poor_naming": [
            "naming",
            "variable name",
        ],
        "excessive_nesting": [
            "nesting",
            "nested",
        ],
        "long_function": [
            "long function",
            "function length",
        ],
    }

    def match(
        self,
        expected_findings: list[dict],
        actual_findings: list[dict],
    ) -> dict:
        true_positives = []
        false_positives = []
        false_negatives = []

        unmatched_actual = actual_findings.copy()

        for expected in expected_findings:
            keywords = self.ISSUE_KEYWORDS.get(
                expected["issue"],
                [],
            )

            matched_finding = None

            for actual in unmatched_actual:
                if actual["category"] != expected["category"]:
                    continue

                if actual["file_path"] != expected["file_path"]:
                    continue

                title = actual["title"].lower()

                is_match = False

                for keyword in keywords:
                    if keyword in title:
                        is_match = True
                        break

                if is_match:
                    matched_finding = actual
                    break

            if matched_finding:
                true_positives.append(matched_finding)
                unmatched_actual.remove(matched_finding)
            else:
                false_negatives.append(expected)

        false_positives = unmatched_actual

        return {
            "true_positives": true_positives,
            "false_positives": false_positives,
            "false_negatives": false_negatives,
        }
