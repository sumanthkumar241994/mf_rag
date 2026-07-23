from app.quality.evaluation.enums import MetricSource, MetricStatus, MetricType
from app.quality.evaluation.evaluator.base_evalutor import BaseEvaluator
from app.quality.evaluation.models.evaluation_context import EvaluationContext
from app.quality.evaluation.models.evaluation_metric import EvaluationMetric
from app.quality.evaluation.models.evaluation_result import EvaluationResult


class LatencyEvaluator(BaseEvaluator):

    async def evaluate(
        self,
        context: EvaluationContext,
    ) -> EvaluationResult:

        latency = context.trace.advisor_generation.first_token_latency_ms

        metric = EvaluationMetric(
            type=MetricType.LATENCY,
            source=MetricSource.TRACE,
            score=1.0 if latency < 3000 else 0.0,
            status=MetricStatus.PASSED if latency < 3000 else MetricStatus.FAILED,
            explanation=f"Response latency: {latency} ms",
        )

        return EvaluationResult(
            metrics=[metric],
        )