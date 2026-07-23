from collections import defaultdict
import uuid

from app.langfuse.models.trace_context import TraceContext
from app.models.feedback import Feedback
from app.quality.evaluation.enums import EvaluationTriggerType
from app.quality.evaluation.evaluation_service import EvaluationService
from app.quality.evaluation.models.evaluation_context import EvaluationContext
from app.unit_of_work.feedback_uow import FeedbackUnitOfWork
from app.unit_of_work.feedback_uow_factory import FeedbackUnitOfWorkFactory


class FeedbackReviewJob:

    MAX_BATCH_SIZE = 5

    def __init__(
        self,
        uow_factory: FeedbackUnitOfWorkFactory,
        evaluation_service: EvaluationService,
    ):
        self._uow_factory = uow_factory
        self._evaluation_service = evaluation_service

    async def execute(self) -> None:

        uow: FeedbackUnitOfWork = self._uow_factory.create()
        async with uow:

            feedbacks = (
                await uow.feedbacks.get_pending_negative_feedbacks()
            )

            if not feedbacks:
                return

            grouped = self._group_by_category(feedbacks)

            for category, items in grouped.items():

                batch = items[: self.MAX_BATCH_SIZE]

                for feedback in batch:

                    context = self._build_context(feedback)

                    await self._evaluation_service.evaluate(context)

                    feedback.evaluation_id = context.evaluation_id


    def _group_by_category(
        self,
        feedbacks: list[Feedback],
    ) -> dict[str, list[Feedback]]:

        grouped: dict[str, list[Feedback]] = defaultdict(list)

        for feedback in feedbacks:
            grouped[feedback.category].append(feedback)

        return grouped

    def _build_context(
        self,
        feedback: Feedback,
    ) -> EvaluationContext:

        return EvaluationContext(
            evaluation_id=uuid.uuid4(),
            conversation=feedback.conversation,
            user_message=feedback.user_message,
            assistant_message=feedback.assistant_message,
            feedback=feedback,
            trace=TraceContext(
                trace_id=feedback.trace_id,
            ),
            trigger_type=EvaluationTriggerType.FEEDBACK,
        )