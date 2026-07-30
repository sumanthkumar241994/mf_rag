from app.core.database import AsyncSessionLocal
from app.unit_of_work.evaluation_uow import EvaluationUnitOfWork


class EvaluationUnitOfWorkFactory:

    async def create(self) -> EvaluationUnitOfWork:
        async with AsyncSessionLocal() as session:
            uow = EvaluationUnitOfWork(session)

            try:
                yield uow
                await uow.commit()
            except Exception:
                await uow.rollback()
                raise