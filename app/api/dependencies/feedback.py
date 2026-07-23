from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.database import get_db
from app.events.publishers.sqs_publisher import SQSEventPublisher
from app.quality.feedback.feedback_service import FeedbackService
from app.repositories.feedback_repository import FeedbackRepository
from app.repositories.message_repository import MessageRepository
from app.unit_of_work.feedback_uow import FeedbackUnitOfWork

def get_feedback_service(
    db: AsyncSession = Depends(get_db),
) -> FeedbackService:

    return FeedbackService(
        uow=FeedbackUnitOfWork(db),
        publisher=SQSEventPublisher()
    )