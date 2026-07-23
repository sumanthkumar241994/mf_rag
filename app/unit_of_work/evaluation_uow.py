from __future__ import annotations

from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories.evaluation_repository import EvaluationRepository
from app.unit_of_work.base import UnitOfWork

class EvaluationUnitOfWork(UnitOfWork):
    def __init__(self, db: AsyncSession):
        self.db = db
        self.evaluations = EvaluationRepository(db)

    async def commit(self):
        await self.db.commit()
    
    async def rollback(self):
        await self.db.rollback()