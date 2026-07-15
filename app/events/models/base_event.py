from dataclasses import dataclass, field
from datetime import timezone, datetime
from uuid import uuid4

from app.events.models.event_priority import EventPriority
from app.events.models.event_types import EventType

@dataclass(slots=True, kw_only=True)
class BaseEvent:
    event_id: str = field(default_factory=lambda: str(uuid4()))
    correlation_id: str | None = None

    event_type: EventType = EventType.BASE
    priority: EventPriority = EventPriority.MEDIUM.value
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    @classmethod
    def from_dict(cls, payload: dict):
        raise NotImplementedError

    @classmethod
    def _base_kwargs(cls, payload: dict) -> dict:
        return {
            "event_id": payload["event_id"],
            "correlation_id": payload["correlation_id"],
            "occurred_at": datetime.fromisoformat(payload["occurred_at"]),
        }
