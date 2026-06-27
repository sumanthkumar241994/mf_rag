from dataclasses import dataclass

from app.dtos.llm.llm_stream_response import LLMStreamResponse
from app.enums.stream_event_type import StreamEventType

@dataclass(slots=True)
class AgentStreamEvent:
    type: StreamEventType
    token: str | None = None
    response: LLMStreamResponse | None = None