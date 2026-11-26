import json
from pathlib import Path

from main import run_audit
from evaluation.finding_matcher import FindingMatcher
from evaluation.metrics import EvaluationMetrics

class Evaluator:
    def __init__(self):
        self.finding_matcher = FindingMatcher()
        self.metrics = EvaluationMetrics()

    def load_expected_findings(self, file_path: Path) -> list[dict]:
        with file_path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        return data["findings"]

    def evaluate(self, sample_project: Path, expected_file: Path) -> dict:
        expected_findings = self.load_expected_findings(expected_file)

        final_state = run_audit(sample_project)
        actual_findings = final_state.get("findings", [])

        match_result = self.finding_matcher.match(
            expected_findings,
            actual_findings
        )

        tp = len(match_result["true_positives"])
        fp = len(match_result["false_positives"])
        fn = len(match_result["false_negatives"])

        metrics = self.metrics.calculate(tp, fp, fn)

        return {
            "expected_findings": expected_findings,
            "actual_findings": actual_findings,
            "matched_findings": match_result["true_positives"],
            "false_positives": match_result["false_positives"],
            "false_negatives": match_result["false_negatives"],
            "metrics": metrics,
        }