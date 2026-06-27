
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from app.api.dependencies.database import get_db
from app.cache import conversation_cache
from app.cache.conversation_cache import ConversationCache
from app.core.config.redis import get_redis
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository
from app.services.conversation_service import ConversationService

def get_conversation_cache(redis: Redis = Depends(get_redis)) -> ConversationCache:
    return ConversationCache(redis)

async def get_conversation_service(
    db: AsyncSession = Depends(get_db), 
    conversation_cache = Depends(get_conversation_cache)
) -> ConversationService:

    return ConversationService(
        conversation_repository=ConversationRepository(db),
        message_repository=MessageRepository(db),
        cache=conversation_cache
    )