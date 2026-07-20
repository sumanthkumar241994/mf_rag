from app.events.handlers.base import EventHandler
from app.events.models.feedback_recieved_event import FeedbackReceivedEvent

import logging
logger = logging.getLogger(__name__)

class FeedbackReceivedHandler(EventHandler[FeedbackReceivedEvent]):
    critical= False
    
    async def handle(
        self,
        event: FeedbackReceivedEvent,
    ) -> None:
        logger.info(
            "Feedback received: %s",
            event.feedback_id,
        )