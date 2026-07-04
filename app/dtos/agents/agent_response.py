from typing import Any
from dataclasses import dataclass, field
from uuid import UUID
from app.schemas.responses.advisor import SourceResponse

@dataclass(slots=True)
class AgentResponse:
    conversation_id: UUID
    answer: str
    sources: list[SourceResponse]

    chunk_count: int | None = None
    response_time_ms: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)