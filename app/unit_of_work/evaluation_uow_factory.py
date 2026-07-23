from app.core.database import AsyncSessionLocal
from app.unit_of_work.evaluation_uow import EvaluationUnitOfWork


class EvaluationUnitOfWorkFactory:

    async def create(self) -> EvaluationUnitOfWork:
        session = AsyncSessionLocal()
        return EvaluationUnitOfWork(session)