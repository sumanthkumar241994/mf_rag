from dataclasses import dataclass

from app.events.models.base_event import BaseEvent

from app.dtos.llm.llm_request import LLMRequest
from app.dtos.llm.llm_usage import LLMUsage
from app.dtos.llm.llm_metrics import LLMMetrics


@dataclass(slots=True)
class LLMGenerationCompletedEvent(BaseEvent):
    request: LLMRequest
    answer: str
    usage: LLMUsage
    metrics: LLMMetrics

