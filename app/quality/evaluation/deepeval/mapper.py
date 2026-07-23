from deepeval.metrics import BaseMetric

from app.quality.evaluation.enums import MetricSource, MetricStatus, MetricType
from app.quality.evaluation.models.evaluation_metric import EvaluationMetric


class DeepEvalMapper:

    @staticmethod
    def to_metric(
        metric_type: MetricType,
        metric: BaseMetric,
    ) -> EvaluationMetric:

        return EvaluationMetric(
            type=metric_type,
            source=MetricSource.LLM_JUDGE,
            status=MetricStatus.PASSED if metric.success else MetricStatus.FAIL,
            score=metric.score,
            explanation=metric.reason,
            metadata={
                "threshold": metric.threshold,
                "success": metric.success,
            },
        )