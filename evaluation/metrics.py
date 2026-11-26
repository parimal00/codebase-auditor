
class EvaluationMetrics:
    def calculate(self, tp: int, fp: int, fn: int) -> dict:
        precision = 0.0
        recall = 0.0
        f1_score = 0.0

        if tp + fp > 0:
            precision = tp / (tp + fp)

        if tp + fn > 0:
            recall = tp / (tp + fn)

        if precision + recall > 0:
            f1_score = (
                2 * precision * recall
            ) / (precision + recall)

        return {
            "true_positives": tp,
            "false_positives": fp,
            "false_negatives": fn,
            "precision": round(precision, 2),
            "recall": round(recall, 2),
            "f1_score": round(f1_score, 2),
        }
