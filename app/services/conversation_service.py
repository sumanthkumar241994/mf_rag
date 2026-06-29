from __future__ import annotations

import logging
from datetime import datetime, timezone
from typing import Any
from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession

from app.cache.conversation_cache import ConversationCache
from app.enums.conversation import ConversationStatus, MessageRole
from app.models.conversation import Conversation
from app.models.message import Message
from app.schemas.conversation.cache_message import CacheMessage
from app.unit_of_work.conversation_uow import ConversationUnitOfWork

logger = logging.getLogger(__name__)

class ConversationService:
    def __init__(
        self, 
        db: AsyncSession,
        uow: ConversationUnitOfWork,
        cache: ConversationCache
    ):  
        self.db=db
        self.uow = uow
        self.cache = cache
    
    def _create_conversation(
        self,
        customer_id: str,
        session_id: UUID,
        workflow: str,
        title: str | None = None,
        metadata: dict[str, Any] | None = None
    ) -> Conversation:
        metadata = metadata or {}

        return Conversation(
            customer_id=customer_id,
            session_id=session_id,
            workflow=workflow,
            title=title,
            status=ConversationStatus.ACTIVE.value,
            metadata_=metadata,
            started_at=datetime.now(timezone.utc)
        )

    def _create_message(
        self,
        conversation_id: UUID,
        sequence_number: int,
        role: MessageRole,
        content: str,
        metadata: dict[str, Any] | None = None
    ) -> Message:
        metadata = metadata or {}

        return Message(
            conversation_id=conversation_id,
            sequence_number=sequence_number,
            role=role,
            content=content,
            metadata_=metadata
        )
    
    async def _update_cache(
        self,
        conversation_id: UUID,
        role: MessageRole,
        content: str,
        metadata: dict[str, Any] | None = None
    ) -> None:
        metadata = metadata or {}

        try:
            await self.cache.append_message(
                conversation_id,
                CacheMessage(
                    role=role,
                    content=content,
                    metadata=metadata
                )
            )
        except Exception as ex:
            logger.error(f"Failed to update the conversation cache for conversation: {conversation_id} and exception: {str(ex)} ")
        
    
    async def create_conversation(
        self,
        customer_id: str,
        session_id: UUID,
        workflow: str,
        title: str | None = None,
        metadata: dict[str, Any] | None = None
    ) -> Conversation:
        """
        Creates a new conversation
        """

        conversation = self._create_conversation(
            customer_id=customer_id,
            session_id=session_id,
            workflow=workflow,
            title=title,
            metadata=metadata
        )

        conversation = await self.uow.conversations.create(conversation)
        logger.info(f"Created conversation for {conversation.id} and workflow: {conversation.workflow}")

        return conversation

    async def get_or_create_conversation(
        self,
        customer_id: str,
        session_id: UUID,
        workflow: str,
        title: str | None = None,
        metadata: dict[str, Any] | None = None
    ) -> Conversation:
        conversation = await self.uow.conversations.get_by_session_id(session_id)

        if conversation:
            return conversation
        
        logger.info(f"Creating new conversation for session: {session_id}")
        return await self.create_conversation(
            customer_id=customer_id,
            session_id=session_id,
            workflow=workflow,
            title=title,
            metadata=metadata
        )

    async def save_message(
        self,
        conversation: Conversation,
        role: MessageRole,
        content: str,
        metadata: dict[str, Any] | None = None
    ) -> Message:
        """
        Saves a conversation message.

        PostgreSQL is the source of truth.
        Redis is updated as a runtime cache.

        Does not commit the transaction.
        """
        metadata = metadata or {}

        last_sqeuence_id = await self.uow.messages.get_last_sequence(conversation.id)

        message = self._create_message(
            conversation_id=conversation.id,
            sequence_number=last_sqeuence_id + 1,
            role=role,
            content=content,
            metadata=metadata
        )

        message = await self.uow.messages.create(message)

        await self._update_cache(
            conversation.id,
            role,
            content,
            metadata
        )

        logger.debug(f"Saved {role} message for conversation {conversation.id}")

        return message

    async def get_recent_context(
        self,
        conversation_id: UUID,
        limit: int = 20,
    ) -> list[CacheMessage]:
        """
        Returns recent conversation messages.

        Cache-aside strategy:

        Redis
        ↓
        PostgreSQL
        ↓
        Redis
        """

        if await self.cache.exists(conversation_id):
            return await self.cache.get_messages(conversation_id)

        logger.debug(f"Conversation cache miss for {conversation_id}")

        messages = await self.uow.messages.get_recent(
            conversation_id,
            limit
        )

        cache_messages = [
            CacheMessage(
                role=message.role,
                content=message.content,
                metadata=message.metadata_
            )
            for message in messages
        ]

        await self.cache.set_messages(conversation_id, cache_messages)

        return cache_messages

    async def complete_conversation(
        self,
        conversation_id: UUID
    ):
        """
        Marks the conversation as completed and clears runtime cache.
        """
        await self.uow.conversations.complete(conversation_id)
        await self.cache.delete(conversation_id)
        logger.info(f"completed conversation: {conversation_id}")
