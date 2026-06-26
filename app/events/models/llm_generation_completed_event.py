from dataclasses import dataclass

from app.events.models.base_event import BaseEvent
from app.events.models.event_priority import EventPriority

from app.dtos.llm.llm_request import LLMRequest
from app.dtos.llm.llm_usage import LLMUsage
from app.dtos.llm.llm_metrics import LLMMetrics


@dataclass(slots=True)
class LLMGenerationCompletedEvent(BaseEvent):
    request: LLMRequest | None = None
    answer: str | None = None
    usage: LLMUsage | None = None
    metrics: LLMMetrics | None = None
    priority: EventPriority = EventPriority.MEDIUM.value
    event_type: str = 'llm.generation.completed'

    @classmethod
    def from_dict(cls, payload: dict) -> "LLMGenerationCompletedEvent":
        return cls(
            event_id=payload["event_id"],
            correlation_id=payload["correlation_id"],
            trace_id=payload.get("trace_id"),
            parent_observation_id=payload.get("parent_observation_id"),
            occurred_at=payload["occurred_at"],
            event_type=payload["event_type"],
            priority=EventPriority(payload["priority"]),

            request=(
                LLMRequest(**payload["request"])
                if payload.get("request")
                else None
            ),

            answer=payload.get("answer"),

            usage=(
                LLMUsage(**payload["usage"])
                if payload.get("usage")
                else None
            ),

            metrics=(
                LLMMetrics(**payload["metrics"])
                if payload.get("metrics")
                else None
            ),
        )


