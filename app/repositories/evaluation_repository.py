from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models import EvaluationModel
from app.repositories.base_repository import BaseRepository


class EvaluationRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def create(
        self,
        evaluation: EvaluationModel,
    ) -> EvaluationModel:
        self.db.add(evaluation)

        await self.db.flush()

        return evaluation

    async def update(
        self,
        evaluation: EvaluationModel,
    ) -> EvaluationModel:
        await self.db.flush()

        return evaluation

    async def get_by_id(
        self,
        evaluation_id: UUID,
    ) -> EvaluationModel | None:
        stmt = (
            select(EvaluationModel)
            .options(selectinload(EvaluationModel.metrics))
            .where(EvaluationModel.id == evaluation_id)
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_message_id(
        self,
        message_id: UUID,
    ) -> EvaluationModel | None:
        stmt = (
            select(EvaluationModel)
            .options(selectinload(EvaluationModel.metrics))
            .where(EvaluationModel.message_id == message_id)
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_conversation_id(
        self,
        conversation_id: UUID,
    ) -> list[EvaluationModel]:
        stmt = (
            select(EvaluationModel)
            .options(selectinload(EvaluationModel.metrics))
            .where(EvaluationModel.conversation_id == conversation_id)
            .order_by(EvaluationModel.created_at.desc())
        )

        result = await self.db.execute(stmt)

        return list(result.scalars().all())

    async def exists_for_message(
        self,
        message_id: UUID,
    ) -> bool:
        stmt = (
            select(EvaluationModel.id)
            .where(EvaluationModel.message_id == message_id)
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none() is not None

    async def delete(
        self,
        evaluation: EvaluationModel,
    ) -> None:
        await self.db.delete(evaluation)

        await self.db.flush()