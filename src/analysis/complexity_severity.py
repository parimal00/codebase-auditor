class ComplexitySeverityEvaluator:

    def evaluate(self, complexity: int) -> str:
        if complexity <= 10:
            return "low"

        if complexity <= 20:
            return "medium"

        return "high"