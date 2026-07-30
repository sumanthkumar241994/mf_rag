from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.dependencies.database import get_db
from app.unit_of_work.conversation_uow import ConversationUnitOfWork


def get_conversation_uow(db: AsyncSession = Depends(get_db)) -> ConversationUnitOfWork:
    return ConversationUnitOfWork(db)