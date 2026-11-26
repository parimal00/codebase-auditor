from pathlib import Path

from rich.console import Console
from rich.table import Table

from evaluation.evaluator import Evaluator

console = Console()


def display_findings(title: str, findings: list[dict], expected: bool = False):
    table = Table(title=title)

    table.add_column("Category")
    table.add_column("File")
    table.add_column("Issue / Title")

    for finding in findings:
        issue = finding["issue"] if expected else finding["title"]

        table.add_row(
            finding["category"],
            finding["file_path"],
            issue
        )

    console.print(table)


def main():
    project_root = Path(__file__).resolve().parent.parent

    sample_project = (
        project_root / "evaluation/datasets/quality/sample_project"
    )

    expected_file = (
        project_root / "evaluation/expected_findings/quality.json"
    )

    evaluator = Evaluator()
    results = evaluator.evaluate(sample_project, expected_file)

    display_findings(
        "Expected Findings",
        results["expected_findings"],
        expected=True
    )

    display_findings(
        "Actual Findings",
        results["actual_findings"]
    )

    display_findings(
        "Matched Findings (True Positives)",
        results["matched_findings"]
    )

    display_findings(
        "False Positives",
        results["false_positives"]
    )

    display_findings(
        "False Negatives",
        results["false_negatives"],
        expected=True
    )

    metrics = results["metrics"]

    console.print("\n[bold cyan]Evaluation Metrics[/bold cyan]")
    console.print(f"True Positives:  {metrics['true_positives']}")
    console.print(f"False Positives: {metrics['false_positives']}")
    console.print(f"False Negatives: {metrics['false_negatives']}")
    console.print(f"Precision:       {metrics['precision']}")
    console.print(f"Recall:          {metrics['recall']}")
    console.print(f"F1 Score:        {metrics['f1_score']}")


if __name__ == "__main__":
    main()