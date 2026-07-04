
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.agents.advisor_agent import AdvisorAgent
from app.api.dependencies.agent import get_advisor_agent
from app.api.dependencies.conversation import get_conversation_service
from app.api.dependencies.database import get_db
from app.orchestration.orchestrator import Orchestrator
from app.services.conversation_service import ConversationService


def get_orchestrator(
    conversation_service: ConversationService=Depends(get_conversation_service), 
    agent: AdvisorAgent = Depends(get_advisor_agent)
) -> Orchestrator:
    return Orchestrator(
        conversation_service=conversation_service,
        agent=agent
        )