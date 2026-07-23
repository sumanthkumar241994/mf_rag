from app.api.dependencies.llm import get_llm_gateway
from app.core.config import settings
from app.notifications.notification_service import NotificationService
from app.notifications.zapier_client import ZapierClient
from app.prompts.evaluator.builder.feedback_insight_prompt_builder import FeedbackInsightPromptBuilder
from app.prompts.registry import PromptRegistry
from app.quality.feedback.evalutors.llm_feedback_insight_evaluator import LLMFeedbackInsightEvaluator
from app.quality.feedback.feedback_insight_analyzer import FeedbackIssueAnalyzer
from app.quality.feedback.feedback_insight_service import FeedbackInsightService
from app.unit_of_work.feedback_insight_uow_factory import FeedbackInsightUnitOfWorkFactory


def get_feedback_insight_service() -> FeedbackInsightService:
    llm_gateway = get_llm_gateway()
    prompt_registry = PromptRegistry()

    prompt_registry.register(
        FeedbackInsightPromptBuilder()
    )

    llm_evaluator = LLMFeedbackInsightEvaluator(
        llm_gateway=llm_gateway,
        prompt_registry=prompt_registry
    )

    uow_factory = FeedbackInsightUnitOfWorkFactory()

    return FeedbackInsightService(
        uow_factory=uow_factory,
        evaluator=llm_evaluator,
        issue_analyzer=FeedbackIssueAnalyzer(),
        notification_service=NotificationService(ZapierClient(settings.FEEDBACK_ZAPIER_WEBHOOK_URL))
    )