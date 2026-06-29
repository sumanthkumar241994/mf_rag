from dataclasses import asdict
import time
from typing import AsyncIterator

from app.agents.base_agent import BaseAgent
from app.enums.stream_event_type import StreamEventType
from app.schemas.requests.chat import ChatRequest
from app.dtos.agents.agent_request import AgentRequest
from app.dtos.agents.agent_response import AgentResponse
from app.enums.conversation import MessageRole
from app.services.conversation_service import ConversationService


class Orchestrator:
    def __init__(self, conversation_service: ConversationService):
        self.conversation_service = conversation_service

    async def run(self, request: ChatRequest, agent: BaseAgent) -> AgentResponse:
        start_time = time.perf_counter() 

        async with self.conversation_service.uow:

            conversation = await self.conversation_service.get_or_create_conversation(
                                customer_id=request.customer_id,
                                session_id=request.session_id,
                                workflow='advisor'
                            )

            await self.conversation_service.save_message(
                conversation=conversation,
                role=MessageRole.USER.value,
                content=request.query
            )

            history = await self.conversation_service.get_recent_context(conversation.id)

            agent_request = AgentRequest(query=request.query, conversation=history)

            response = await agent.run(agent_request)

            await self.conversation_service.save_message(
                conversation=conversation,
                role=MessageRole.ASSISTANT.value,
                content=response.answer,
                metadata=response.metadata
            )
            response.response_time_ms = round((time.perf_counter()-start_time) *1000)

        return response
    
    async def stream(self, request: ChatRequest, agent: BaseAgent) -> AsyncIterator[str]:
        
        async with self.conversation_service.uow:
            conversation = await self.conversation_service.get_or_create_conversation(
                                customer_id=request.customer_id,
                                session_id=request.session_id,
                                workflow='advisor'
                            )
            await self.conversation_service.save_message(
                conversation=conversation,
                role=MessageRole.USER.value,
                content=request.query
            )

            history = await self.conversation_service.get_recent_context(conversation.id)

            agent_request = AgentRequest(query=request.query, conversation=history)

            stream_response = None 

            async for event in agent.stream(agent_request):
                if event.type == StreamEventType.TOKEN.value:
                    yield event.token
                elif event.type == StreamEventType.COMPLETED.value:
                    stream_response = event.response

            await self.conversation_service.save_message(
                conversation=conversation,
                role=MessageRole.ASSISTANT.value,
                content=stream_response.answer,
                metadata={
                    "usage": asdict(stream_response.usage),
                    "metrics": asdict(stream_response.metrics)
                }

            )