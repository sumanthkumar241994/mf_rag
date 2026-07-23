from app.core.database import AsyncSessionLocal
from app.unit_of_work.feedback_uow import FeedbackUnitOfWork


class FeedbackUnitOfWorkFactory:

    async def create(self) -> FeedbackUnitOfWork:
        session = AsyncSessionLocal()
        return FeedbackUnitOfWork(session)