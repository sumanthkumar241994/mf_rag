from typing import AsyncIterator

from app.dtos.agents.agent_response import AgentResponse
from app.dtos.agents.stream_event import AgentStreamEvent
from app.dtos.request_context import RequestContext
from app.orchestration.orchestrator import Orchestrator

from app.observability.tracing import trace_workflow


class ChatService:
    def __init__(
        self,
        orchestrator: Orchestrator,
    ):
        self._orchestrator = orchestrator

    @trace_workflow("chat")
    async def chat(
        self,
        request: RequestContext,
    ) -> AgentResponse:
        return await self._orchestrator.run(request=request)

    @trace_workflow(
        "stream_chat",
        input_mapper=lambda self, request: {
            "query": request.query,
            "customer_id": request.customer_id,
            "has_conversation": request.conversation_id is not None,
        },
    )
    async def stream(
        self,
        request: RequestContext,
    ) -> AsyncIterator[AgentStreamEvent]:
        async for event in self._orchestrator.stream(request=request):
            yield event