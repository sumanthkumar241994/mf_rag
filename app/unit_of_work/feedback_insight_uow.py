from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.conversation_repository import ConversationRepository
from app.repositories.feedback_issue_repository import FeedbackIssueRepository
from app.repositories.feedback_occurence_repository import FeedbackOccurrenceRepository
from app.repositories.feedback_repository import FeedbackRepository
from app.repositories.message_repository import MessageRepository
from app.unit_of_work.base import UnitOfWork

class FeedbackInsightUnitOfWork(UnitOfWork):
    def __init__(self, db: AsyncSession):
        self.db = db
        self.feedbacks = FeedbackRepository(db)
        self.feedback_issues = FeedbackIssueRepository(db)
        self.feedback_occurences = FeedbackOccurrenceRepository(db)
        self.messages = MessageRepository(db)
        self.conversations = ConversationRepository(db)

    async def commit(self):
        await self.db.commit()
    
    async def rollback(self):
        await self.db.rollback()
