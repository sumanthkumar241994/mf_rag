from app.models.message import Message
from app.notifications.notification_service import NotificationService
from app.quality.feedback.enums.insight import FeedbackIssueAction
from app.quality.feedback.evalutors.llm_feedback_insight_evaluator import LLMFeedbackInsightEvaluator
from app.quality.feedback.feedback_insight_analyzer import FeedbackIssueAnalyzer
from app.quality.feedback.models.feedback import Feedback
from app.quality.feedback.models.feedback_insight_context import (
    FeedbackInsightContext,
)
from app.unit_of_work.feedback_insight_uow import FeedbackInsightUnitOfWork
from app.unit_of_work.feedback_insight_uow_factory import FeedbackInsightUnitOfWorkFactory


class FeedbackInsightService:

    def __init__(
        self,
        uow_factory: FeedbackInsightUnitOfWorkFactory,
        evaluator: LLMFeedbackInsightEvaluator,
        issue_analyzer: FeedbackIssueAnalyzer,
        notification_service: NotificationService,
    ):
        self._uow_factory = uow_factory
        self._evaluator = evaluator
        self._issue_analyzer = issue_analyzer
        self._notification_service = notification_service

    async def process(
        self,
        feedback: Feedback,
    ) -> None:

        self._uow: FeedbackInsightUnitOfWork = await self._uow_factory.create()

        async with self._uow:

            context = await self._build_context(feedback)

            insight = await self._evaluator.evaluate(context)

            result = await self._issue_analyzer.analyze(
                feedback=feedback,
                insight=insight,
                uow=self._uow
            )

            feedback.feedback_issue_id = result.issue.id

            await self._uow.feedbacks.save(feedback)

            await self._uow.commit()

        # Decide Create/Update inside NotificationService
        await self._notification_service.publish_feedback_issue(
            issue=result.issue,
            occurrence=result.occurrence,
            insight=insight,
            feedback=feedback,
            action=result.action,
        )

    async def _build_context(
        self,
        feedback: Feedback,
    ) -> FeedbackInsightContext:

        conversation = await self._uow.conversations.get_by_id(
            feedback.conversation_id,
        )

        assistant_message = await self._uow.messages.get_by_id(
            feedback.message_id,
        )

        if assistant_message is None:
            raise ValueError("Assistant message not found.")

        user_message = await self._get_previous_user_message(
            assistant_message,
        )

        return FeedbackInsightContext(
            feedback=feedback,
            conversation=conversation,
            user_message=user_message,
            assistant_message=assistant_message,
        )

    async def _get_previous_user_message(
        self,
        assistant_message: Message,
    ) -> Message | None:

        return await self._uow.messages.get_previous_user_message(
            conversation_id=assistant_message.conversation_id,
            sequence_number=assistant_message.sequence_number,
        )