import logging

from app.events.handlers.base import EventHandler
from app.events.models.conversation_summary_generate_event import ConversationSummaryGenerateEvent
from app.services.conversation_summary_service import ConversationSummaryService


logger = logging.getLogger(__name__)


class ConversationSummaryHandler(EventHandler[ConversationSummaryGenerateEvent]):
    """
    Generates an incremental conversation summary.
    """

    critical = False

    def __init__(self, summary_service: ConversationSummaryService):
        self._summary_service = summary_service

    async def handle(self, event: ConversationSummaryGenerateEvent) -> None:
        logger.info("Generating summary for conversation %s", event.conversation_id)

        await self._summary_service.generate(
            conversation_id=event.conversation_id,
        )