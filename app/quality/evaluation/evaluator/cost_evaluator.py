

from app.quality.evaluation.enums import MetricSource, MetricStatus, MetricType
from app.quality.evaluation.evaluator.base_evalutor import BaseEvaluator
from app.quality.evaluation.models.evaluation_context import EvaluationContext
from app.quality.evaluation.models.evaluation_metric import EvaluationMetric
from app.quality.evaluation.models.evaluation_result import EvaluationResult


class CostEvaluator(BaseEvaluator):

    def __init__(
        self,
        warning_cost: float = 0.02,
        max_cost: float = 0.05,
    ):
        self._warning_cost = warning_cost
        self._max_cost = max_cost

    async def evaluate(
        self,
        context: EvaluationContext,
    ) -> EvaluationResult:

        generation = context.trace.advisor_generation

        if generation is None:
            return EvaluationResult()

        cost = generation.total_cost or 0.0

        if cost <= self._warning_cost:
            score = 1.0
            status = MetricStatus.PASSED

        elif cost <= self._max_cost:
            score = 0.5
            status = MetricStatus.WARNING

        else:
            score = 0.0
            status = MetricStatus.FAILED

        metric = EvaluationMetric(
            type=MetricType.COST,
            source=MetricSource.TRACE,
            score=score,
            status=status,
            explanation=(
                f"Total cost: ${cost:.6f}"
            ),
            metadata={
                "model": generation.model,
                "cost": cost,
                "input_tokens": generation.input_tokens,
                "output_tokens": generation.output_tokens,
                "total_tokens": generation.total_tokens,
                "warning_cost": self._warning_cost,
                "max_cost": self._max_cost,
            },
        )

        return EvaluationResult(
            metrics=[metric],
        )