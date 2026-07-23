from deepeval.test_case import LLMTestCase

from app.business.advisor.enums.tool_type import ToolType
from app.quality.evaluation.deepeval.adapter import DeepEvalAdapter
from app.quality.evaluation.enums import MetricType
from app.quality.evaluation.evaluator.base_evalutor import BaseEvaluator
from app.quality.evaluation.models.evaluation_context import EvaluationContext
from app.quality.evaluation.models.evaluation_metric import EvaluationMetric
from app.quality.evaluation.models.evaluation_result import EvaluationResult



class DeepEvalEvaluator(BaseEvaluator):

    def __init__(
        self,
        adapter: DeepEvalAdapter,
    ) -> None:
        self._adapter = adapter

    async def evaluate(
        self,
        context: EvaluationContext,
    ) -> list[EvaluationMetric]:

        if context.trace.retrieval and context.trace.retrieval.tool == ToolType.DOCUMENT_SEARCH.value:
            retrieval_context = [
                chunk.content
                for chunk in context.trace.retrieval.chunks
            ]
        else:
            retrieval_context = [
                context.trace.advisor_generation.user_prompt
            ] if context.trace.advisor_generation else []

        test_case = LLMTestCase(
            input=context.user_message.content,
            actual_output=context.assistant_message.content,
            retrieval_context=retrieval_context
        )

        metrics: list[EvaluationMetric] = []

        for metric_type in (
            MetricType.ANSWER_RELEVANCY,
            # MetricType.FAITHFULNESS,
            # MetricType.CONTEXTUAL_RELEVANCY,
            # MetricType.CONTEXTUAL_PRECISION,
            # MetricType.HALLUCINATION,
            # MetricType.BIAS,
            # MetricType.TOXICITY

        ):
            metrics.append(
                await self._adapter.evaluate(
                    metric_type=metric_type,
                    test_case=test_case,
                )
            )

        return EvaluationResult(
            metrics=metrics,
        )