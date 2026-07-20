from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.feedback import Feedback as FeedbackModel
from app.quality.feedback.models.feedback import Feedback


class FeedbackRepository:

    def __init__(self, session: AsyncSession):
        self._session = session

    async def get_by_message(
        self,
        customer_id: UUID,
        message_id: UUID,
    ) -> Feedback | None:

        stmt = (
            select(FeedbackModel).where(
                FeedbackModel.customer_id == customer_id,
                FeedbackModel.message_id == message_id,
            )
        )

        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            return None

        return Feedback.model_validate(model)

    async def save(
        self,
        feedback: Feedback,
    ) -> Feedback:

        stmt = (
            select(FeedbackModel).where(
                FeedbackModel.customer_id == feedback.customer_id,
                FeedbackModel.message_id == feedback.message_id,
            )
        )

        result = await self._session.execute(stmt)
        model = result.scalar_one_or_none()

        if model is None:
            model = FeedbackModel(**feedback.model_dump())
            self._session.add(model)
        else:
            update_data = feedback.model_dump(
                exclude={
                    "id",
                    "customer_id",
                    "conversation_id",
                    "message_id",
                    "trace_id",
                    "created_at",
                },
                exclude_none=False,
            )

            for field, value in update_data.items():
                setattr(model, field, value)

        await self._session.flush()
        await self._session.refresh(model)

        return Feedback.model_validate(model)