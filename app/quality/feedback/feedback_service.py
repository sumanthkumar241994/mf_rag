from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.events.models.feedback_recieved_event import FeedbackReceivedEvent
from app.events.publishers.base import EventPublisher
from app.events.publishers.sqs_publisher import SQSEventPublisher
from app.models.message import MessageRole
from app.quality.feedback.enums.feedback_signal import FeedbackSignal
from app.quality.feedback.exceptions import FeedbackMessageNotFoundException, FeedbackNotAllowedException, FeedbackUnauthorizedException, InvalidFeedbackException
from app.quality.feedback.models.feedback import Feedback
from app.quality.feedback.models.submit_feedback_request import SubmitFeedbackRequest
from app.unit_of_work.feedback_uow import FeedbackUnitOfWork

import logging

logger = logging.getLogger(__name__)

class FeedbackService:

    def __init__(
        self,
        uow: FeedbackUnitOfWork,
        publisher: EventPublisher
    ):
        self._uow = uow
        self._publisher = publisher

    async def submit_feedback(
        self,
        customer_id: UUID,
        request: SubmitFeedbackRequest,
    ) -> Feedback:

        async with self._uow:

            message = await self._validate_message(
                customer_id=customer_id,
                message_id=request.message_id,
            )

            self._validate_feedback(request)

            existing = await self._uow.feedbacks.get_by_message(
                customer_id=customer_id,
                message_id=request.message_id,
            )

            now = datetime.now(UTC)

            if existing:
                feedback = existing.model_copy(
                    update={
                        "signal": request.signal,
                        "reason": request.reason,
                        "comment": request.comment,
                        "updated_at": now,
                    }
                )
            else:
                feedback = Feedback(
                    id=uuid4(),
                    customer_id=customer_id,
                    conversation_id=message.conversation_id,
                    message_id=message.id,
                    trace_id=message.trace_id,
                    signal=request.signal,
                    reason=request.reason,
                    comment=request.comment,
                    created_at=now,
                    updated_at=now,
                )

            feedback = await self._uow.feedbacks.save(feedback)

            await self._uow.commit()

            try:
    
                await self._publisher.publish(
                    FeedbackReceivedEvent(
                        feedback_id=str(feedback.id),
                        customer_id=feedback.customer_id,
                        conversation_id=str(feedback.conversation_id),
                        message_id=str(feedback.message_id),
                        signal=feedback.signal.value,
                        reason=feedback.reason.value if feedback.reason else None,
                    )
                )
            except Exception as ex:
                logger.error(f"Could not publish feedback recieved event: {str(ex)}")

            return feedback

    async def _validate_message(
        self,
        customer_id: UUID,
        message_id: UUID,
    ):
        message = await self._uow.messages.get_by_id(message_id)

        if message is None:
            raise FeedbackMessageNotFoundException()

        if message.role != MessageRole.ASSISTANT:
            raise FeedbackNotAllowedException()

        return message

    def _validate_feedback(
        self,
        request: SubmitFeedbackRequest,
    ) -> None:

        if (
            request.signal == FeedbackSignal.POSITIVE
            and request.reason is not None
        ):
            raise InvalidFeedbackException(
                "Positive feedback cannot have a reason."
            )

        if (
            request.signal == FeedbackSignal.NEGATIVE
            and request.reason is None
        ):
            raise InvalidFeedbackException(
                "Negative feedback requires a reason."
            )

        if request.comment:
            comment = request.comment.strip()

            if len(comment) < 3:
                raise InvalidFeedbackException(
                    "Comment must contain at least 3 characters."
                )