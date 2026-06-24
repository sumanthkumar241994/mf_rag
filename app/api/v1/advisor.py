from fastapi import APIRouter, Depends

from app.schemas.requests.advisor import AdvisorRequest

from app.api.dependencies.advisor import get_advisor_service
from app.advisor.advisor_service import AdvisorService

from app.dtos.agents.agent_response import AgentResponse

router = APIRouter()


@router.post("/chat",response_model=AgentResponse)
async def chat(request: AdvisorRequest, advisor_service: AdvisorService=Depends(get_advisor_service)):
    advisor_response = await advisor_service.chat(
        query=request.query
    )

    return advisor_response