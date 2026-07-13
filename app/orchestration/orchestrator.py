from dataclasses import asdict
import time
from typing import AsyncIterator

from app.agents.advisor_agent import AdvisorAgent
from app.core.middleware.request_context_vars import trace_id_ctx
from app.dtos.agents.stream_event import AgentStreamEvent
from app.dtos.request_context import RequestContext
from app.enums.stream_event_type import StreamEventType
from app.dtos.agents.agent_response import AgentResponse
from app.enums.conversation import MessageRole
from app.services.conversation_service import ConversationService
from app.workflows.advisor.advisor_state import AdvisorState

import app.observability.langfuse_helper as LangfuseHelper


class Orchestrator:
    def __init__(self, conversation_service: ConversationService, agent: AdvisorAgent):
        self.conversation_service = conversation_service
        self.agent = agent
    async def run(self, request: RequestContext) -> AgentResponse:
        start_time = time.perf_counter() 

        async with self.conversation_service.uow:

            conversation = await self.conversation_service.get_or_create_conversation(
                                customer_id=request.customer_id,
                                conversation_id=request.conversation_id,
                                workflow='advisor'
                            )

            if request.query:
                await self.conversation_service.save_message(
                    conversation=conversation,
                    role=MessageRole.USER.value,
                    content=request.query or request.workflow_resume
                )

            trace_id = LangfuseHelper.get_trace_id()

            request.conversation_id = conversation.id

            trace_id_ctx.set(trace_id)

            history = await self.conversation_service.get_recent_context(conversation.id)

            state = AdvisorState(
                request=request, 
                history=history,
                trace_id=LangfuseHelper.get_trace_id(),
            )

            if request.workflow_resume:
                response = await self.agent.resume(state)
            else:
                response = await self.agent.run(state)

            if response.answer:
                await self.conversation_service.save_message(
                    conversation=conversation,
                    role=MessageRole.ASSISTANT.value,
                    content=response.answer,
                    metadata=response.metadata
                )
            response.response_time_ms = round((time.perf_counter()-start_time) *1000)
            
        return response
    
    async def stream(self, request: RequestContext) -> AsyncIterator[AgentStreamEvent]:
        
        async with self.conversation_service.uow:
            conversation = await self.conversation_service.get_or_create_conversation(
                                customer_id=request.customer_id,
                                conversation_id=request.conversation_id,
                                workflow='advisor'
                            )
            await self.conversation_service.save_message(
                conversation=conversation,
                role=MessageRole.USER.value,
                content=request.query
            )

            history = await self.conversation_service.get_recent_context(conversation.id)

            trace_id = conversation.trace_id if request.workflow_resume else LangfuseHelper.get_trace_id()

            state = AdvisorState(
                request=request,
                history=history,
                trace_id=trace_id
            )

            yield AgentStreamEvent(
                    type=StreamEventType.SESSION.value,
                    metadata={
                        "conversation_id": str(conversation.id),
                        "trace_id": str(trace_id)
                    }
                )
            stream_response = None 

            if request.workflow_resume:
                stream = self.agent.resume_stream(state)
            else:
                stream = self.agent.stream(state)

            async for event in stream:
                yield event

                if event.type == StreamEventType.COMPLETED.value:
                    stream_response = event.response

            if stream_response:
                metadata = {}

                if stream_response.usage:
                    metadata['llm_usage'] = asdict(stream_response.usage)
                if stream_response.metrics:
                    metadata['llm_metrics'] = asdict(stream_response.metrics)

                await self.conversation_service.save_message(
                    conversation=conversation,
                    role=MessageRole.ASSISTANT.value,
                    content=stream_response.answer,
                    metadata=metadata

                )