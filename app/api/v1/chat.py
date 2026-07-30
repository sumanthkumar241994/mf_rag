import json

from fastapi import APIRouter, Depends, Response
from fastapi.responses import StreamingResponse

from app.api.dependencies.chat import get_chat_service
from app.api.dependencies.request_context import build_request_context

from app.core.middleware.request_context_vars import trace_id_ctx
from app.dtos.agents.agent_response import AgentResponse
from app.dtos.request_context import RequestContext
from app.services.chat_service import ChatService


router = APIRouter()


@router.post(
    "",
    response_model=AgentResponse,
)
async def chat(
    response: Response,
    request: RequestContext = Depends(build_request_context),
    chat_service: ChatService = Depends(get_chat_service),
) -> AgentResponse:

    agent_response = await chat_service.chat(
        request=request,
    )

    if trace_id := trace_id_ctx.get():
        response.headers["X-Trace-Id"] = trace_id

    return agent_response


@router.post("/stream")
async def stream_chat(
    request: RequestContext = Depends(build_request_context),
    chat_service: ChatService = Depends(get_chat_service),
):
    async def event_generator():
        async for event in chat_service.stream(request):
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
            "X-Accel-Buffering": "no",
        },
    )