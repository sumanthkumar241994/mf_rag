from deepeval.metrics import BaseMetric
from deepeval.test_case import LLMTestCase

from app.quality.evaluation.enums import MetricType
from app.quality.evaluation.models.evaluation_metric import EvaluationMetric

from .llm import AdvisorJudgeLLM
from .mapper import DeepEvalMapper


class DeepEvalAdapter:

    def __init__(
        self,
        metrics: dict[MetricType, BaseMetric],
    ) -> None:
        self._metrics = metrics

    async def evaluate(
        self,
        metric_type: MetricType,
        test_case: LLMTestCase,
    ) -> EvaluationMetric:

        metric = self._metrics[metric_type]

        await metric.a_measure(test_case)

        return DeepEvalMapper.to_metric(
            metric_type=metric_type,
            metric=metric,
        )