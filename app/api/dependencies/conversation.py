
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from app.api.dependencies.database import get_db
from app.api.dependencies.unit_of_work import get_conversation_uow
from app.cache.conversation_cache import ConversationCache
from app.core.config.redis import get_redis
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository
from app.services.conversation_service import ConversationService
from app.unit_of_work.conversation_uow import ConversationUnitOfWork

def get_conversation_cache(redis: Redis = Depends(get_redis)) -> ConversationCache:
    return ConversationCache(redis)

async def get_conversation_service(
    db: AsyncSession = Depends(get_db), 
    uow: ConversationUnitOfWork = Depends(get_conversation_uow),
    conversation_cache = Depends(get_conversation_cache)
) -> ConversationService:

    return ConversationService(
        db=db,
        uow=uow,
        cache=conversation_cache
    )