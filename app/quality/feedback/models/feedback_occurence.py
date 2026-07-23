from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class FeedbackOccurrence(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID | None = None

    issue_id: UUID
    feedback_id: UUID
    conversation_id: UUID
    message_id: UUID

    created_at: datetime