from __future__ import annotations

from datetime import datetime, timezone
from typing import Optional
from uuid import UUID

from sqlalchemy import delete, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.conversation import Conversation
from app.enums.conversation import ConversationStatus

class ConversationRepository:
    """
    Repository is responsible for conversation persistance
    
    This layer should only have database acess
    No business logic
    """

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, conversation: Conversation) -> Conversation:
        self.db.add(conversation)
        await self.db.flush()
        await self.db.refresh(conversation)
        return conversation

    async def get_by_id(self, conversation_id: UUID) -> Optional[Conversation]:
        stmt = select(Conversation).where(Conversation.id == conversation_id)
        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()
        

    async def get_active_conversation(self, customer_id: str, workflow: str) -> Optional[Conversation]:
        stmt = select(Conversation).where(
                Conversation.customer_id == customer_id, 
                Conversation.workflow == workflow,
                Conversation.status == ConversationStatus.ACTIVE.value
                ).order_by(
                    Conversation.created_at.desc()
                )

        result = await self.db.execute(stmt)
        return result.scalars().first()        
    
    async def update(self, conversation: Conversation) -> Conversation:
        await self.db.flush()
        await self.db.refresh(conversation)
        return conversation
    
    async def update_title(self, conversation_id: UUID, title: str):
        stmt = update(Conversation).where(Conversation.id == conversation_id).values(title=title, updated_at=datetime.now(timezone.utc))
        await self.db.execute(stmt)
    
    async def update_current_agent(self, conversation_id: UUID, agent: str):
        stmt = update(Conversation).where(Conversation.id == conversation_id).values(current_agent=agent, updated_at=datetime.now(timezone.utc))
        await self.db.execute(stmt)
    
    async def update_current_node(self, conversation_id: UUID, node: str):
        stmt = update(Conversation).where(Conversation.id == conversation_id).values(current_node=node, updated_at=datetime.now(timezone.utc))
        await self.db.execute(stmt)

    async def increment_message_count(self, conversation_id: UUID):
        conversation = await self.get_by_id(conversation_id=conversation_id)

        if not conversation:
            return
        
        conversation.message_count += 1
        conversation.last_message_at = datetime.now(timezone.utc)
        await self.db.flush()

    async def complete(self, conversation_id: UUID):
        stmt = update(Conversation).where(
            Conversation.id == conversation_id
            ).values(
                status=ConversationStatus.COMPLETED.value, 
                updated_at=datetime.now(timezone.utc),
                completed_at=datetime.now(timezone.utc)
            )
        await self.db.execute(stmt)

    async def fail(self, conversation_id: UUID):
        stmt = update(Conversation).where(
            Conversation.id == conversation_id
            ).values(
                status=ConversationStatus.FAILED.value, 
                updated_at=datetime.now(timezone.utc)
            )
        await self.db.execute(stmt)

    async def abandon(self, conversation_id: UUID):
        stmt = update(Conversation).where(
            Conversation.id == conversation_id
            ).values(
                status=ConversationStatus.ABANDONED.value, 
                updated_at=datetime.now(timezone.utc)
            )
        await self.db.execute(stmt)

    async def delete(self, conversation_id: UUID):
        stmt = delete(Conversation).where(
            Conversation.id == conversation_id
            )
        await self.db.execute(stmt)


    
        