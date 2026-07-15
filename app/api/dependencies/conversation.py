
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from app.api.dependencies.database import get_db
from app.api.dependencies.llm import get_llm_gateway
from app.api.dependencies.unit_of_work import get_conversation_uow
from app.cache.conversation_cache import ConversationCache
from app.core.config.redis import get_redis
from app.core.database.session import AsyncSessionLocal
from app.events.publishers.sqs_publisher import SQSEventPublisher
from app.prompts.builder.conversation_title_prompt_builder import ConversationTitlePromptBuilder
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository
from app.services.conversation_service import ConversationService
from app.services.conversation_summary_service import ConversationSummaryService
from app.services.conversation_title_service import ConversationTitleService
from app.unit_of_work.conversation_uow import ConversationUnitOfWork
from app.unit_of_work.conversation_uow_factory import ConversationUnitOfWorkFactory

def get_conversation_cache(redis: Redis = Depends(get_redis)) -> ConversationCache:
    return ConversationCache(redis)

async def get_conversation_service(
    uow: ConversationUnitOfWork = Depends(get_conversation_uow),
    conversation_cache = Depends(get_conversation_cache)
) -> ConversationService:

    return ConversationService(
        uow=uow,
        cache=conversation_cache,
        publisher=SQSEventPublisher()
    )


def build_conversation_title_service() -> ConversationTitleService:
    return ConversationTitleService(
        uow_factory=ConversationUnitOfWorkFactory(),
        llm_gateway=get_llm_gateway()
    )

def build_conversation_summary_service() -> ConversationSummaryService:
    return ConversationSummaryService(
        uow_factory=ConversationUnitOfWorkFactory(),
        llm_gateway=get_llm_gateway()
    )
