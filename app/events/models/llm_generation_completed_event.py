from dataclasses import dataclass

from app.events.models.base_event import BaseEvent

from app.dtos.llm.llm_request import LLMRequest
from app.dtos.llm.llm_usage import LLMUsage
from app.dtos.llm.llm_metrics import LLMMetrics


@dataclass(slots=True)
class LLMGenerationCompletedEvent(BaseEvent):
    request: LLMRequest | None = None
    answer: str | None = None
    usage: LLMUsage | None = None
    metrics: LLMMetrics | None = None

    event_type: str = 'llm.generation.completed'
