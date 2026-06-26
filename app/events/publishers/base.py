from abc import ABC, abstractmethod

from app.events.models.base_event import BaseEvent

class EventPublisher(ABC):
    
    @abstractmethod
    async def publish(str, event: BaseEvent) -> None:
        """
        Publish an event to the configured transport
        """
        raise NotImplementedError