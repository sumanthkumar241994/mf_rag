from app.dtos.llm.llm_request import LLMRequest
from app.llm_gateway.enums.model_profile import ModelProfile
from app.llm_gateway.llm_gateway import LLMGateway
from app.notifications.models import NotificationSeverity
from app.prompts.enums import PromptType
from app.prompts.evaluator.builder.feedback_insight_prompt_builder import FeedbackInsightPromptBuilder
from app.prompts.registry import PromptRegistry
from app.quality.feedback.enums.insight import IssueCategory, RootCause
from app.quality.feedback.evalutors.base import FeedbackInsightEvaluator
from app.quality.feedback.models.feedback_insight import FeedbackInsight
from app.quality.feedback.models.feedback_insight_context import FeedbackInsightContext
from app.quality.feedback.models.feedback_insight_result import FeedbackInsightResult


class LLMFeedbackInsightEvaluator(FeedbackInsightEvaluator):

    def __init__(
        self,
        llm_gateway: LLMGateway,
        prompt_registry: PromptRegistry,
    ) -> None:
        self._llm_gateway = llm_gateway
        self._prompt_registry = prompt_registry

    async def evaluate(
        self,
        context: FeedbackInsightContext,
    ) -> FeedbackInsightResult:
        prompt = self._build_prompt(context)

        request = LLMRequest(
            system_prompt=prompt.system_prompt,
            user_prompt=prompt.user_prompt,
            response_model=FeedbackInsightResult,
            temperature=0,
        )

        # response = await self._llm_gateway.generate(request, model_profile=ModelProfile.JUDGE)

        # result =  response.structured_output

        result = FeedbackInsightResult(
            category=IssueCategory.BUSINESS,
            root_cause=RootCause.BUSINESS_INCORRECT_RECOMMENDATION,
            severity=NotificationSeverity.CRITICAL,
            confidence=0.95,
            summary = "Test case",
            recommendation="test"
        )

        return FeedbackInsight(
            feedback_id=context.feedback.id,
            category=result.category,
            root_cause=result.root_cause,
            severity=result.severity,
            confidence=result.confidence,
            summary=result.summary,
            recommendation=result.recommendation,
        )
    
    def _build_prompt(
        self,
        context: FeedbackInsightContext,
    ):
        builder = self._prompt_registry.get(
            PromptType.FEEDBACK_INSIGHT,
        )

        return builder.build(context)