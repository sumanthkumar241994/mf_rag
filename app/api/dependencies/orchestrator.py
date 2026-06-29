
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.api.dependencies.conversation import get_conversation_service
from app.api.dependencies.database import get_db
from app.orchestration.orchestrator import Orchestrator
from app.services.conversation_service import ConversationService


def get_orchestrator(conversation_service: ConversationService=Depends(get_conversation_service)) -> Orchestrator:
    return Orchestrator(conversation_service)