from dataclasses import asdict

from langfuse.api import PromptType

from app.dtos.llm.llm_request import LLMRequest
from app.llm_gateway.llm_gateway import LLMGateway
from app.prompts.registry import PromptRegistry
from app.quality.evaluation.judges.base import BaseJudge
from app.quality.evaluation.judges.models import PlannerJudgeResponse
from app.quality.evaluation.models.evaluation_context import EvaluationContext
from app.quality.evaluation.models.judge_models import JudgeResult


class PlannerJudge(BaseJudge):
    """LLM-as-a-Judge for evaluating planner routing decisions."""

    def __init__(
        self,
        llm_gateway: LLMGateway,
        prompt_registry: PromptRegistry,
    ) -> None:
        self._llm_gateway = llm_gateway
        self._prompt_registry = prompt_registry

    async def judge(
        self,
        context: EvaluationContext,
    ) -> JudgeResult:
        prompt = self._build_prompt(context)

        response = await self._llm_gateway.generate(
            LLMRequest(
                system_prompt=prompt.system_prompt,
                user_prompt=prompt.user_prompt,
                temperature=0,
                response_model=PlannerJudgeResponse,
            )
        )

        result: PlannerJudgeResponse = response.structured_output

        return self._build_result(result)

    def _build_prompt(
        self,
        context: EvaluationContext,
    ):
        builder = self._prompt_registry.get(
            PromptType.PLANNER_JUDGE,
        )

        return builder.build(context)

    @staticmethod
    def _build_result(
        result: PlannerJudgeResponse,
    ) -> JudgeResult:
        return JudgeResult(
            score=result.overall_score,
            status=result.status,
            explanation=result.explanation,
            issues=result.issues,
            metadata=asdict(result),
        )