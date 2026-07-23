from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies.database import get_db
from app.services.feedback_webhook_service import FeedbackWebhookService
from app.unit_of_work.feedback_insight_uow import FeedbackInsightUnitOfWork


def get_feedback_webhook_service(db: AsyncSession=Depends(get_db)) -> FeedbackWebhookService:
    return FeedbackWebhookService(
        uow=FeedbackInsightUnitOfWork(db)
    )