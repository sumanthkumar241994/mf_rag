from uuid import UUID

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    customer_id: str | None = Field(default=None, exclude=True)
    session_id: UUID | None = Field(default=None, exclude=True)
    query: str = Field(..., min_length=1)

