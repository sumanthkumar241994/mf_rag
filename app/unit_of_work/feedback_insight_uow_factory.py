from app.core.database import AsyncSessionLocal
from app.unit_of_work.feedback_insight_uow import FeedbackInsightUnitOfWork

class FeedbackInsightUnitOfWorkFactory:

    async def create(self) -> FeedbackInsightUnitOfWork:
        async with AsyncSessionLocal() as session:
            uow = FeedbackInsightUnitOfWork(session)

            try:
                yield uow
                await uow.commit()
            except Exception:
                await uow.rollback()
                raise