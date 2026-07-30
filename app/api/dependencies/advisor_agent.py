from redis.asyncio import Redis
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.advisor_agent import AdvisorAgent
from app.api.dependencies.database import get_database, get_db
from app.api.dependencies.policy_repository import get_policy_repository
from app.api.dependencies.rest_api_client import get_rest_api_client
from app.api.dependencies.streaming_response_assembler import (
    get_streaming_assembler,
)

from app.compliance.repository.policy_repository import PolicyRepository
from app.compliance.response.streaming.streaming_response_assembler import (
    StreamingResponseAssembler,
)
from app.composition.advisor_composition import AdvisorComposition
from app.core.config.redis import get_redis
from app.infrastructure.api_client.rest_client import RestApiClient
from app.infrastructure.workflow.workflow_checkpointer import workflow_checkpointer
from app.services.advisor_service import AdvisorService


_advisor: AdvisorComposition | None = None

def advisor_agent() -> AdvisorAgent:

    global _advisor

    if _advisor is None:
        _advisor = AdvisorComposition(
            database=get_database(),
            redis=get_redis(),
            rest_api_client=get_rest_api_client(),
            policy_repository=get_policy_repository(),
            checkpointer=workflow_checkpointer.checkpointer,
            streaming_assembler=get_streaming_assembler(),
        )

    return _advisor.agent


def get_advisor_service() -> AdvisorService:
    return _advisor
    
def get_advisor_agent() -> AdvisorAgent:
    return advisor_agent()