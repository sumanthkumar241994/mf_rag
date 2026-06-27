from typing import Any
from dataclasses import dataclass, field
from app.schemas.responses.advisor import SourceResponse

@dataclass(slots=True)
class AgentResponse:
    answer: str
    sources: list[SourceResponse]

    chunk_count: int | None = None
    response_time_ms: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)