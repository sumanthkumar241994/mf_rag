from dataclasses import asdict
import time
from typing import AsyncIterator

from app.agents.advisor_agent import AdvisorAgent
from app.compliance.response.streaming import stream_state
from app.core.middleware.request_context_vars import trace_id_ctx
from app.dtos.agents.stream_event import AgentStreamEvent
from app.dtos.request_context import RequestContext
from app.enums.stream_event_type import StreamEventType
from app.dtos.agents.agent_response import AgentResponse
from app.enums.conversation import MessageRole
from app.models.message import Message
from app.services.conversation_service import ConversationService
from app.workflows.advisor.advisor_state import AdvisorState

import app.observability.langfuse_helper as LangfuseHelper


class Orchestrator:
    def __init__(self, conversation_service: ConversationService, agent: AdvisorAgent):
        self.conversation_service = conversation_service
        self.agent = agent

    async def run(self, request: RequestContext) -> AgentResponse:
        start_time = time.perf_counter() 

        trace_id = LangfuseHelper.get_trace_id()

        async with self.conversation_service.uow:

            conversation = await self.conversation_service.get_or_create_conversation(
                                customer_id=request.customer_id,
                                conversation_id=request.conversation_id,
                                workflow='advisor'
                            )

            if request.workflow_resume:
                await self.conversation_service.add_resume_message(
                    conversation=conversation,
                    content=request.workflow_resume,
                    trace_id=trace_id   
                )
            else:
                await self.conversation_service.add_user_message(
                    conversation=conversation,
                    content=request.query,
                    trace_id=trace_id
                )

            request.conversation_id = conversation.id

            trace_id_ctx.set(trace_id)

            history = await self.conversation_service.get_recent_context(conversation.id)

            state = AdvisorState(
                request=request, 
                history=history,
                trace_id=trace_id,
            )

            if request.workflow_resume:
                response = await self.agent.resume(state)
            else:
                response = await self.agent.run(state)

            if response.answer:
                await self.conversation_service.add_assistant_message(
                    conversation=conversation,
                    content=response.answer,
                    trace_id=trace_id,
                    metadata=response.metadata
                )
            response.response_time_ms = round((time.perf_counter()-start_time) *1000)
            
        return response
    
    async def stream(self, request: RequestContext) -> AsyncIterator[AgentStreamEvent]:
        trace_id = LangfuseHelper.get_trace_id()

        async with self.conversation_service.uow:
            conversation = await self.conversation_service.get_or_create_conversation(
                                customer_id=request.customer_id,
                                conversation_id=request.conversation_id,
                                workflow='advisor'
                            )

            if request.workflow_resume:
                await self.conversation_service.add_resume_message(
                    conversation=conversation,
                    content=request.workflow_resume,
                    trace_id=trace_id,
                )
            else:
                await self.conversation_service.add_user_message(
                    conversation=conversation,
                    content=request.query,
                    trace_id=trace_id,
                )

            history = await self.conversation_service.get_recent_context(conversation.id)
            
            request.conversation_id = conversation.id

            trace_id_ctx.set(trace_id)

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
            workflow_interrupt = None

            if request.workflow_resume:
                stream = self.agent.resume_stream(state)
            else:
                stream = self.agent.stream(state)

            async for event in stream:
                yield event

                if event.type == StreamEventType.COMPLETED.value:
                    stream_response = event.response

                elif event.type == StreamEventType.WORKFLOW_INTERRUPT.value:
                    workflow_interrupt = event.workflow_interrupt
                    break

            if stream_response:
                metadata = {}

                if stream_response.usage:
                    metadata['llm_usage'] = asdict(stream_response.usage)
                if stream_response.metrics:
                    metadata['llm_metrics'] = asdict(stream_response.metrics)

                message: Message =  await self.conversation_service.add_assistant_message(
                    conversation=conversation,
                    content=stream_response.answer,
                    trace_id=trace_id,
                    metadata=metadata

                )

                yield AgentStreamEvent(
                    type=StreamEventType.MESSAGE_SAVED.value,
                    metadata={
                        "message_id": str(message.id),
                    },
                )
                    

            elif workflow_interrupt:
                await self.conversation_service.add_interrupt_message(
                    conversation=conversation,
                    capability=workflow_interrupt.capability.value,
                    questions=workflow_interrupt.questions,
                    trace_id=trace_id,
                )