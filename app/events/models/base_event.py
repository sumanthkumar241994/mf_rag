from dataclasses import dataclass, field
from datetime import timezone, datetime
from uuid import uuid4

from app.events.models.event_priority import EventPriority

@dataclass(slots=True)
class BaseEvent:
    event_id: str = field(default_factory=lambda: str(uuid4()))
    correlation_id: str = field(default_factory=lambda: str(uuid4()))
    event_type: str = ""
    priority: EventPriority = EventPriority.MEDIUM
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))