# app/events/handlers/base.py
from abc import ABC, abstractmethod
from typing import Generic, TypeVar

from app.events.models.base_event import BaseEvent

EventT = TypeVar("EventT", bound=BaseEvent)

class EventHandler(ABC, Generic[EventT]):
    """
    Base interface for all event handlers.

    A handler is responsible for processing a single domain event.
    Multiple handlers can subscribe to the same event.
    """
    critical: bool = False
    
    @abstractmethod
    async def handle(self, event: EventT):
        """
        Process a published event.

        Raises:
            Exception:
                Implementations may raise exceptions. The dispatcher
                decides whether to retry, dead-letter, or ignore them.
        """
        raise NotImplementedError