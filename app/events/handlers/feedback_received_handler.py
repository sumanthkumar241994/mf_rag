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

        # 🚨 Negative Feedback Received

        # Customer ID     : xxxx
        # Conversation ID : xxxx
        # Message ID      : xxxx
        # Time            : 2026-07-23 11:15 UTC

        # Reason          : Generic Response
        # Comment         : "It ignored my existing portfolio."

        # Advisor Response
        # ----------------------------------------------------
        # Based on your investment goals, I recommend...
        # ----------------------------------------------------

        # Actions
        # • View Conversation
        # • View Langfuse Trace
        # • View Feedback