# app/events/factory/event_factory.py

from app.events.models.base_event import BaseEvent
from app.events.models.llm_generation_completed_event import LLMGenerationCompletedEvent

class EventFactory:
    _events = {
        "llm.generation.completed": LLMGenerationCompletedEvent
    }

    @classmethod
    def from_dict(cls, payload: dict) -> BaseEvent:
        event_type = payload.get("event_type")
        event_class = cls._events.get(event_type)
        print(event_type, event_class)
        if event_class is None:
            raise ValueError(f"Unsupported event type: {event_type}")
        
        return event_class.from_dict(payload)