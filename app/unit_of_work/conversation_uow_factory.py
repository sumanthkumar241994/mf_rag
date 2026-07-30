# app/unit_of_work/conversation_uow_factory.py
from contextlib import asynccontextmanager
from app.core.database import AsyncSessionLocal
from app.unit_of_work.conversation_uow import ConversationUnitOfWork


class ConversationUnitOfWorkFactory:

    @asynccontextmanager
    async def create(self):
        async with AsyncSessionLocal() as session:
            uow = ConversationUnitOfWork(session)

            try:
                yield uow
                await uow.commit()
            except Exception:
                await uow.rollback()
                raise