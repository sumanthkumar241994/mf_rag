import asyncio
from collections import defaultdict

from app.events.handlers.base import EventHandler
from app.events.models.base_event import BaseEvent
import logging

logger = logging.getLogger(__name__)

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
            
        results = await asyncio.gather(*(handler.handle(event) for handler in handlers), return_exceptions=True)

        critical_errors = []

        for handler, result in zip(handlers, results):
            if isinstance(result, Exception):
                logger.exception(f"Handler: {handler.__class__.__name__} failed. event_id: {event.event_id}", exc_info=result)
            
            if handler.critical and result:
                critical_errors.append(result)
        
        if handler.critical and critical_errors:
            print(f"Critical Errors: {critical_errors}")
            raise result