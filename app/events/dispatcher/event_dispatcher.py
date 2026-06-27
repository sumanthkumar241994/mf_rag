import asyncio
from collections import defaultdict

from app.events.handlers.base import EventHandler
from app.events.models.base_event import BaseEvent

class EventDispatcher:
    """
    Dispatches a domain event to all registered handlers
    """
    def __init__(self):
        self._handlers: dict[str, list[EventHandler]] = defaultdict(list)
    
    def register(self, event_type: str, handler: EventHandler):
        """
        Register a handler for an event type
        """
        self._handlers[event_type].append(handler)
    
    async def dispatch(self, event: BaseEvent):
        """
        Dispatch an event to all registered handlers
        """
        handlers = self._handlers.get(event.event_type, [])
        if not handlers:
            return

        await asyncio.gather(*(handler.handle(event) for handler in handlers), return_exceptions=True)