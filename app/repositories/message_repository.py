from __future__ import annotations

from typing import Optional
from uuid import UUID

from sqlalchemy import func, select, delete
from sqlalchemy.ext.asyncio import AsyncSession

from app.enums.conversation import MessageRole, MessageType
from app.models.message import Message

class MessageRepository:
    """
    Repository responsible for message persistance
    """
    def __init__(self, db: AsyncSession):
        print(db)
        self.db = db
    
    async def create(self, message: Message) -> Message:
        self.db.add(message)
        await self.db.flush()
        await self.db.refresh(message)

        return message
    
    async def create_many(self, messages: list[Message]) -> list[Message]:
        self.db.add_all(messages)
        await self.db.flush()
        
        for message in messages:
            await self.db.refresh(message)

        return messages
    
    async def get_messages(self, conversation_id: UUID, offset: int = 0, limit: int | None = None) -> list[Message]:
        stmt = select(Message).where(Message.conversation_id == conversation_id).order_by(Message.sequence_number).offset(offset)

        if limit:
            stmt = stmt.limit(limit)
        
        result = await self.db.execute(stmt)
        return result.scalars().all()


    async def get_by_id(self, message_id: UUID) -> Optional[Message]:
        stmt = select(Message).where(Message.id == message_id)
        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()
    
    async def get_recent(self, conversation_id: UUID, limit: int = 20) -> list[Message] :
        stmt = select(Message).where(
            Message.conversation_id==conversation_id
        ).order_by(
            Message.sequence_number.desc()
        ).limit(limit)

        result = await self.db.execute(stmt)

        messages = result.scalars().all()

        # returns oldest -> newest
        return list(reversed(messages))

    async def get_all(self, conversation_id: UUID) -> list[Message]:
        stmt = select(Message).where(
            Message.conversation_id==conversation_id
        ).order_by(
            Message.sequence_number
        )

        result = await self.db.execute(stmt)
        
        return result.scalars().all()
        
    async def get_last_message(self, conversation_id: UUID) -> Optional[Message]:
        stmt = select(Message).where(Message.conversation_id==conversation_id).order_by(Message.sequence_number.desc()).limit(1)
        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    # async def get_last_sequence(self, conversation_id: UUID) -> int:
    #     stmt = select(func.max(Message.sequence_number)).where(Message.conversation_id == conversation_id)

    #     result = await self.db.execute(stmt)
    #     sequence = result.scalar_one()

    #     return sequence or 0

    async def count(self, conversation_id: UUID) -> int:
        stmt = select(func.count(Message.id)).where(Message.conversation_id==conversation_id)

        result = await self.db.execute(stmt)

        return result.scalar_one()

    async def delete(self, message_id: UUID):
        await self.db.execute(delete(Message).where(Message.id == message_id))

    async def delete_by_conversation(self, conversation_id: UUID):
        await self.db.execute(delete(Message).where(Message.conversation_id == conversation_id))

    async def get_messages_for_title(
    self,
    conversation_id: UUID,
    limit: int = 10,
    ) -> list[Message]:
        """
        Returns the first few meaningful conversation messages for title generation.

        Excludes system-generated events such as interrupts, summaries, and titles.
        """

        stmt = (
            select(Message)
            .where(
                Message.conversation_id == conversation_id,
                Message.role.in_(
                    [
                        MessageRole.USER,
                        MessageRole.ASSISTANT,
                    ]
                ),
                Message.message_type.in_(
                    [
                        MessageType.TEXT,
                        MessageType.RESUME,
                    ]
                ),
            )
            .order_by(Message.sequence_number)
            .limit(limit)
        )
        result = await self.db.execute(stmt)

        return result.scalars().all()

    async def get_messages_after_sequence(
        self,
        conversation_id: UUID,
        sequence_number: int,
        limit: int | None = None,
    ) -> list[Message]:
        """
        Returns all conversation messages after the given sequence number.

        Used for incremental conversation summaries.
        """

        stmt = (
            select(Message)
            .where(
                Message.conversation_id == conversation_id,
                Message.sequence_number > sequence_number,
            )
            .order_by(Message.sequence_number)
        )

        if limit is not None:
            stmt = stmt.limit(limit)

        result = await self.db.execute(stmt)

        return result.scalars().all()

    async def count_after_sequence(
    self,
    conversation_id: UUID,
    sequence_number: int,
    ) -> int:
        """
        Returns the number of messages after a given sequence.
        """

        stmt = (
            select(func.count(Message.id))
            .where(
                Message.conversation_id == conversation_id,
                Message.sequence_number > sequence_number,
            )
        )

        result = await self.db.execute(stmt)

        return result.scalar_one()