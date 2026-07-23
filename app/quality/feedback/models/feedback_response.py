from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict

from app.quality.feedback.enums.feedback_reason import FeedbackReason
from app.quality.feedback.enums.feedback_signal import FeedbackSignal



class FeedbackResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    message_id: UUID
    signal: FeedbackSignal
    reason: FeedbackReason | None
    comment: str | None
    updated_at: datetime