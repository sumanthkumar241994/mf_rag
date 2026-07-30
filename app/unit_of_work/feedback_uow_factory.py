from app.core.database import AsyncSessionLocal
from app.unit_of_work.feedback_uow import FeedbackUnitOfWork


class FeedbackUnitOfWorkFactory:

    async def create(self) -> FeedbackUnitOfWork:
        async with AsyncSessionLocal() as session:
            uow = FeedbackUnitOfWork(session)

            try:
                yield uow
                await uow.commit()
            except Exception:
                await uow.rollback()
                raise