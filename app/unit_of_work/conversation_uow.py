from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.conversation_repository import ConversationRepository
from app.repositories.conversation_summary_repository import ConversationSummaryRepository
from app.repositories.message_repository import MessageRepository
from app.unit_of_work.base import UnitOfWork

class ConversationUnitOfWork(UnitOfWork):
    def __init__(self, db: AsyncSession):
        self.db = db
        self.conversations = ConversationRepository(db)
        self.messages = MessageRepository(db)
        self.summaries = ConversationSummaryRepository(db)

    async def commit(self):
        await self.db.commit()
    
    async def rollback(self):
        await self.db.rollback()
