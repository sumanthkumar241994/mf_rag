from app.events.handlers.base import EventHandler
from app.events.models.conversation_title_generate_event import ConversationTitleGenerateEvent
import logging

from app.services.conversation_title_service import ConversationTitleService
logger = logging.getLogger(__name__)


class ConversationTitleHandler(EventHandler[ConversationTitleGenerateEvent]):
    critical = False

    def __init__(
        self,
        title_service: ConversationTitleService,
    ):
        self._title_service = title_service

    async def handle(self, event: ConversationTitleGenerateEvent,) -> None:
        logger.info(
            "Generating title for conversation %s",
            event.conversation_id,
        )

        await self._title_service.generate(
            conversation_id=event.conversation_id,
        )