from dataclasses import dataclass
from app.schemas.responses.advisor import SourceResponse

@dataclass(slots=True)
class AgentResponse:
    answer: str
    sources: list[SourceResponse]

    chunk_count: int | None = None
    response_time_ms: int | None = None