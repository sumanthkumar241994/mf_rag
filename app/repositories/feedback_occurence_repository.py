from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.feedback_occurence import FeedbackOccurrenceModel
from app.quality.feedback.models.feedback_occurence import FeedbackOccurrence



class FeedbackOccurrenceRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    async def save(
        self,
        occurrence: FeedbackOccurrence,
    ) -> FeedbackOccurrence:

        model = FeedbackOccurrenceModel(
            **occurrence.model_dump(),
        )

        self.db.add(model)

        await self.db.flush()
        await self.db.refresh(model)

        return FeedbackOccurrence.model_validate(model)

    async def get_by_feedback_id(
        self,
        feedback_id,
    ) -> FeedbackOccurrence | None:

        stmt = (
            select(FeedbackOccurrenceModel)
            .where(
                FeedbackOccurrenceModel.feedback_id == feedback_id,
            )
        )

        result = await self.db.execute(stmt)

        model = result.scalar_one_or_none()

        if model is None:
            return None

        return FeedbackOccurrence.model_validate(model)