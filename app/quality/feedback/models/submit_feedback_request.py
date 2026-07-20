from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field, model_validator

from app.quality.feedback.enums.feedback_reason import FeedbackReason
from app.quality.feedback.enums.feedback_signal import FeedbackSignal


class SubmitFeedbackRequest(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
        str_strip_whitespace=True,
    )

    message_id: UUID
    signal: FeedbackSignal
    reason: FeedbackReason | None = None
    comment: str | None = Field(
        default=None,
        max_length=1000,
    )

    @model_validator(mode="after")
    def validate_feedback(self) -> "SubmitFeedbackRequest":
        if (
            self.signal == FeedbackSignal.NEGATIVE
            and self.reason is None
        ):
            raise ValueError(
                "Reason is required for negative feedback."
            )

        if (
            self.signal == FeedbackSignal.POSITIVE
            and self.reason is not None
        ):
            raise ValueError(
                "Reason is only allowed for negative feedback."
            )

        return self