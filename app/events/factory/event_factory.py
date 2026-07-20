# app/events/factory/event_factory.py

from app.events.models.base_event import BaseEvent
from app.events.models.conversation_summary_generate_event import ConversationSummaryGenerateEvent
from app.events.models.conversation_title_generate_event import ConversationTitleGenerateEvent
from app.events.models.event_types import EventType
from app.events.models.feedback_recieved_event import FeedbackReceivedEvent
from app.events.models.llm_generation_completed_event import LLMGenerationCompletedEvent
from app.events.models.observation_complated_event import ObservationCompletedEvent

class EventFactory:
    _events = {
        EventType.LLM_GENERATION_COMPLETED: LLMGenerationCompletedEvent,
        EventType.CONVERSATION_TITLE_GENERATE : ConversationTitleGenerateEvent,
        EventType.CONVERSATION_SUMMARY_GENERATE: ConversationSummaryGenerateEvent,
        EventType.FEEDBACK_RECEIVED: FeedbackReceivedEvent,
        EventType.OBSERVATION_COMPLETED: ObservationCompletedEvent
    }

    @classmethod
    def from_dict(cls, payload: dict) -> BaseEvent:
        event_type = payload.get("event_type")
        event_class = cls._events.get(event_type)
        if event_class is None:
            raise ValueError(f"Unsupported event type: {event_type}")
        
        return event_class.from_dict(payload)