from dataclasses import dataclass, field
from typing import Any

from app.events.models.base_event import BaseEvent
from app.events.models.event_priority import EventPriority
from app.events.models.event_types import EventType


@dataclass(slots=True)
class ObservationCompletedEvent(BaseEvent):
    trace_id: str | None = None
    parent_observation_id: str | None = None

    name: str = ""
    input: Any | None = None
    output: Any | None = None
    metadata: dict[str, Any] = field(default_factory=dict)

    priority: EventPriority = EventPriority.MEDIUM.value
    event_type: str = EventType.OBSERVATION_COMPLETED.value

    @classmethod
    def from_dict(cls, payload: dict) -> "ObservationCompletedEvent":
        return cls(
            event_id=payload["event_id"],
            correlation_id=payload["correlation_id"],
            occurred_at=payload["occurred_at"],
            trace_id=payload.get("trace_id"),
            parent_observation_id=payload.get("parent_observation_id"),
            name=payload["name"],
            input=payload.get("input"),
            output=payload.get("output"),
            metadata=payload.get("metadata", {}),
            priority=EventPriority(payload["priority"]),
            event_type=payload["event_type"],
        )