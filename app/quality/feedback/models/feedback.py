from datetime import datetime
from uuid import UUID
from pydantic import BaseModel, ConfigDict

from app.quality.feedback.enums.feedback_reason import FeedbackReason
from app.quality.feedback.enums.feedback_signal import FeedbackSignal


class Feedback(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: UUID
    customer_id: str
    conversation_id: UUID
    message_id: UUID
    trace_id: UUID | None = None

    signal: FeedbackSignal
    reason: FeedbackReason | None = None
    comment: str | None = None

    created_at: datetime
    updated_at: datetime