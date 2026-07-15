from email import message
from uuid import UUID

from app.llm_gateway.llm_gateway import LLMGateway
from app.dtos.llm.llm_request import LLMRequest
from app.prompts.builder.conversation_title_prompt_builder import ConversationTitlePromptBuilder
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository
from app.unit_of_work.conversation_uow_factory import ConversationUnitOfWorkFactory


class ConversationTitleService:
    """
    Generates and persists a conversation title.

    Idempotent:
        - If a title already exists, no work is performed.
    """

    def __init__(
        self,
        uow_factory: ConversationUnitOfWorkFactory,
        llm_gateway: LLMGateway
    ):
        self._uow_factory = uow_factory
        self._llm_gateway = llm_gateway
        self._prompt_builder = ConversationTitlePromptBuilder()

    async def generate(self, conversation_id: UUID) -> None:
        uow = await self._uow_factory.create()

        async with uow:

            conversation = await uow.conversations.get_by_id(
                conversation_id
            )

            if conversation is None:
                return

            # Idempotent
            if conversation.title:
                return

            messages = await uow.messages.get_messages_for_title(
                conversation_id
            )

            if not messages:
                return

            request = self._prompt_builder.build(messages)

            response = await self._llm_gateway.generate(request)

            title = response.answer.strip()

            if not title:
                return

            await uow.conversations.update_title(
                conversation_id=conversation_id,
                title=title,
            )