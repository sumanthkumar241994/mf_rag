from dataclasses import dataclass, field
from datetime import timezone, datetime
from uuid import uuid4

@dataclass(slots=True)
class BaseEvent:
    event_id: str = field(default_factory=lambda: str(uuid4()))
    event_type: str = ""
    occurred_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))