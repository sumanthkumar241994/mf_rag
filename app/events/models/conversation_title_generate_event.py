from dataclasses import dataclass
from uuid import UUID
from app.events.models.base_event import BaseEvent
from app.events.models.event_priority import EventPriority
from app.events.models.event_types import EventType

@dataclass(slots=True, kw_only=True)
class ConversationTitleGenerateEvent(BaseEvent):
    conversation_id: UUID
    event_type: EventType = EventType.CONVERSATION_TITLE_GENERATE
    priority: EventPriority = EventPriority.LOW.value

    @classmethod
    def from_dict(cls, payload: dict):
        return cls(
            **cls._base_kwargs(payload),
            conversation_id=UUID(payload["conversation_id"]),
        )