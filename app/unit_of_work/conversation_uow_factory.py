# app/unit_of_work/conversation_uow_factory.py

from app.core.database import AsyncSessionLocal
from app.unit_of_work.conversation_uow import ConversationUnitOfWork


class ConversationUnitOfWorkFactory:

    async def create(self) -> ConversationUnitOfWork:
        session = AsyncSessionLocal()
        return ConversationUnitOfWork(session)