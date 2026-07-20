from dataclasses import dataclass
from uuid import UUID

from app.events.models.base_event import BaseEvent
from app.events.models.event_priority import EventPriority
from app.events.models.event_types import EventType
from app.quality.feedback.enums.feedback_reason import FeedbackReason
from app.quality.feedback.enums.feedback_signal import FeedbackSignal


@dataclass(slots=True, kw_only=True)
class FeedbackReceivedEvent(BaseEvent):
    feedback_id: UUID
    customer_id: str
    conversation_id: UUID
    message_id: UUID

    signal: FeedbackSignal
    reason: FeedbackReason | None = None
    comment: str | None = None

    event_type: EventType = EventType.FEEDBACK_RECEIVED
    priority: EventPriority = EventPriority.LOW.value

    @classmethod
    def from_dict(cls, payload: dict):
        return cls(
            **cls._base_kwargs(payload),
            feedback_id=UUID(payload["feedback_id"]),
            customer_id=str(payload["customer_id"]),
            conversation_id=UUID(payload["conversation_id"]),
            message_id=UUID(payload["message_id"]),
            signal=FeedbackSignal(payload["signal"]),
            reason=(
                FeedbackReason(payload["reason"])
                if payload.get("reason")
                else None
            ),
            comment=payload.get("comment"),
        )