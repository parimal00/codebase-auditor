from typing import List, Union
from src.schemas.ast_dto import ParsedFileDTO, FunctionDTO
from src.schemas.findings import Finding


class ComplexityRule:
    """Deterministic quality rule to identify functions exceeding cyclomatic complexity thresholds.

    Reads precomputed complexity metrics directly from parsed AST DTOs without reparsing
    source code or recalculating complexity.
    """

    def __init__(
        self,
        medium_threshold: int = 10,
        high_threshold: int = 20,
    ):
        self.medium_threshold = medium_threshold
        self.high_threshold = high_threshold

    def analyze(self, parsed_files: List[Union[ParsedFileDTO, dict]]) -> List[Finding]:
        findings: List[Finding] = []

        for file_data in parsed_files:
            # Handle both DTO and legacy dict gracefully
            if isinstance(file_data, dict):
                file_path = file_data.get("file_path", "")
                if file_data.get("error"):
                    continue
                functions = file_data.get("functions", [])
            else:
                file_path = file_data.file_path
                if file_data.error:
                    continue
                functions = file_data.functions

            for func in functions:
                if isinstance(func, dict):
                    complexity = func.get("cyclomatic_complexity", 1)
                    qname = func.get("qualified_name", func.get("name", "unknown"))
                else:
                    complexity = func.cyclomatic_complexity
                    qname = func.qualified_name

                if complexity <= self.medium_threshold:
                    continue

                severity = (
                    "medium" if complexity <= self.high_threshold
                    else "high"
                )

                findings.append(
                    Finding(
                        category="quality",
                        severity=severity,
                        file_path=file_path,
                        title="High cyclomatic complexity",
                        description=(
                            f"Function '{qname}' has a "
                            f"cyclomatic complexity of {complexity} "
                            f"(threshold: {self.medium_threshold}). "
                            "Consider breaking it into smaller functions "
                            "with more focused responsibilities."
                        ),
                    )
                )

        return findings
