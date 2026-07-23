from app.core.database import AsyncSessionLocal
from app.unit_of_work.feedback_insight_uow import FeedbackInsightUnitOfWork

class FeedbackInsightUnitOfWorkFactory:

    async def create(self) -> FeedbackInsightUnitOfWork:
        session = AsyncSessionLocal()
        return FeedbackInsightUnitOfWork(session)