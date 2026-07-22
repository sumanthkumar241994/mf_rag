import time

from app.quality.evaluation.evaluator_registry import EvaluatorRegistry
from app.quality.evaluation.models.evaluation_context import EvaluationContext
from app.quality.evaluation.models.evaluation_metric import EvaluationMetric
from app.quality.evaluation.models.evaluation_result import EvaluationResult

class EvaluationService:

    def __init__(
        self,
        registry: EvaluatorRegistry,
    ):
        self._registry = registry

    async def evaluate(
        self,
        context: EvaluationContext,
    ) -> EvaluationResult:

        start = time.perf_counter()

        metrics: list[EvaluationMetric] = []

        for evaluator in self._registry.evaluators:

            result = await evaluator.evaluate(context)

            metrics.extend(result.metrics)

        duration = int((time.perf_counter() - start) * 1000)

        scores = [
            metric.score
            for metric in metrics
            if metric.score is not None
        ]

        overall_score = (
            sum(scores) / len(scores)
            if scores
            else None
        )

        return EvaluationResult(
            metrics=metrics,
            overall_score=overall_score,
            duration_ms=duration,
        )