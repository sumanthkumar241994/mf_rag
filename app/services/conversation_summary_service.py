from uuid import UUID

from app.models.conversation_summary import ConversationSummary
from app.prompts.builder.conversation_summary_prompt_builder import ConversationSummaryPromptBuilder
from app.unit_of_work.conversation_uow_factory import (
    ConversationUnitOfWorkFactory,
)
from app.llm_gateway.llm_gateway import LLMGateway


class ConversationSummaryService:

    def __init__(
        self,
        uow_factory: ConversationUnitOfWorkFactory,
        llm_gateway: LLMGateway,
    ):
        self._uow_factory = uow_factory
        self._llm_gateway = llm_gateway
        self._prompt_builder = ConversationSummaryPromptBuilder()

    async def generate(self, conversation_id: UUID) -> None:

        uow = await self._uow_factory.create()

        async with uow:

            latest_summary = await uow.summaries.get_latest(conversation_id)

            latest_version = (
                latest_summary.version
                if latest_summary
                else 0
            )

            latest_sequence = (
                latest_summary.message_end_sequence
                if latest_summary
                else 0
            )

            messages = await uow.messages.get_messages_after_sequence(
                conversation_id=conversation_id,
                sequence_number=latest_sequence,
            )

            if not messages:
                return

            request = self._prompt_builder.build(
                previous_summary=(
                    latest_summary.summary
                    if latest_summary
                    else None
                ),
                messages=messages,
            )

            response = await self._llm_gateway.generate(request)

            summary = response.answer.strip()

            if not summary:
                return

            conversation_summary = ConversationSummary(
                conversation_id=conversation_id,
                version=latest_version + 1,
                start_sequence=latest_sequence + 1,
                end_sequence=messages[-1].sequence_number,
                summary=summary,
                model=response.metrics.model
                if response.metrics
                else None,
            )

            await uow.summaries.create(
                conversation_summary
            )