

from app.quality.evaluation.enums import MetricSource, MetricType
from app.quality.evaluation.evaluator.base_evalutor import BaseEvaluator
from app.quality.evaluation.judges.planner_judge import PlannerJudge
from app.quality.evaluation.models.evaluation_context import EvaluationContext
from app.quality.evaluation.models.evaluation_metric import EvaluationMetric


class PlannerEvaluator(BaseEvaluator):
    """Evaluates planner quality using an LLM Judge."""

    def __init__(
        self,
        planner_judge: PlannerJudge,
    ) -> None:
        self._planner_judge = planner_judge

    async def evaluate(
        self,
        context: EvaluationContext,
    ) -> EvaluationMetric:

        result = await self._planner_judge.judge(context)

        return EvaluationMetric(
            type=MetricType.PLANNER,
            source=MetricSource.LLM_JUDGE,
            status=result.status,
            score=result.score,
            explanation=result.explanation,
            metadata=result.metadata,
        )