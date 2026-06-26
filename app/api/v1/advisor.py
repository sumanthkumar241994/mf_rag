from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

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

@router.post("/chat/stream")
async def stream_chat(request: AdvisorRequest, advisor_service: AdvisorService=Depends(get_advisor_service)):
    async def event_generator():
        async for token in advisor_service.stream(query=request.query):
            yield f"data: {token}\n\n"
        yield "event:done\ndata: [DONE]\n\n"
    
    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )