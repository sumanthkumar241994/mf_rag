from fastapi import APIRouter, Depends

from app.schemas.requests.advisor import AdvisorRequest
from app.schemas.responses.advisor import AdvisorResponse
from app.api.dependencies.advisor import get_advisor_service
from app.advisor.advisor_service import AdvisorService

router = APIRouter()


@router.post("/chat",response_model=AdvisorResponse)
async def chat(request: AdvisorRequest, advisor_service: AdvisorService=Depends(get_advisor_service)):
    advisor_response = await advisor_service.ask(
        query=request.query,
        top_k=request.top_k,
        scheme_name=request.scheme_name,
        document_type=request.document_type
    )

    return advisor_response