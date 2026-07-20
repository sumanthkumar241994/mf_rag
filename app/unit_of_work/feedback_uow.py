from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.feedback_repository import FeedbackRepository
from app.repositories.message_repository import MessageRepository
from app.unit_of_work.base import UnitOfWork

class FeedbackUnitOfWork(UnitOfWork):
    def __init__(self, db: AsyncSession):
        self.db = db
        self.feedbacks = FeedbackRepository(db)
        self.messages = MessageRepository(db)

    async def commit(self):
        await self.db.commit()
    
    async def rollback(self):
        await self.db.rollback()