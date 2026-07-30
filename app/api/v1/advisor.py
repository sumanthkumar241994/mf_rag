import json
from fastapi import APIRouter, Depends, Response
from fastapi.responses import StreamingResponse

from app.api.dependencies.advisor_agent import get_advisor_service
from app.core.middleware.request_context_vars import trace_id_ctx
from app.dtos.request_context import RequestContext

from app.api.dependencies.request_context import build_request_context
from app.services.advisor_service import AdvisorService

from app.dtos.agents.agent_response import AgentResponse

import app.observability.langfuse_helper as LangfuseHelper

router = APIRouter()


@router.post("/chat",response_model=AgentResponse)
async def chat(
    response: Response,
    request: RequestContext = Depends(build_request_context), 
    advisor_service: AdvisorService=Depends(get_advisor_service)
) -> AgentResponse:
    advisor_response = await advisor_service.chat(
        request=request
    )

    if trace_id := trace_id_ctx.get():
        response.headers['X-Trace-Id'] = trace_id

    return advisor_response

# version 1
# @router.post("/chat/stream")
# async def stream_chat(
#     response: Response,
#     request: RequestContext = Depends(build_request_context), 
#     advisor_service: AdvisorService=Depends(get_advisor_service)
# ):
#     async def event_generator():
#         async for token in advisor_service.stream(request):
#             yield f"data: {token}\n\n"
#         yield "event:done\ndata: [DONE]\n\n"


#         if trace_id := trace_id_ctx.get():
#             response.headers['X-Trace-Id'] = trace_id
    
#     return StreamingResponse(
#         event_generator(),
#         media_type="text/event-stream",
#         headers={
#             "Cache-Control": "no-cache",
#             "Connection": "keep-alive",
#             "X-Accel-Buffering": "no"
#         }
#     )


@router.post("/chat/stream")
async def stream_chat(
    response: Response,
    request: RequestContext = Depends(build_request_context), 
    advisor_service: AdvisorService=Depends(get_advisor_service)
):
    async def event_generator():
        async for event in advisor_service.stream(request):
            yield (
                f"event: {event.type}\n"
                f"data: {json.dumps(event.to_dict())}\n\n"
            )

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no"
        }
    )