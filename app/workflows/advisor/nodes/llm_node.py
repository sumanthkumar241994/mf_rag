from typing import AsyncIterator
from app.dtos.agents.stream_event import AgentStreamEvent
from app.dtos.llm.llm_request import LLMRequest
from app.enums.stream_event_type import StreamEventType
from app.llm_gateway.llm_gateway import LLMGateway
from app.workflows.advisor.advisor_state import AdvisorState


class LLMNode:
    """
    Executes the final LLM generation.
    """
    def __init__(self, llm_gateway: LLMGateway):
        self._llm_gateway = llm_gateway
    
    async def __call__(self, state: AdvisorState) -> AdvisorState:
        if state.prompt is None:
            return state
        
        state.llm_response = await self._llm_gateway.generate(
            LLMRequest(
                system_prompt=state.prompt.system_prompt,
                user_prompt=state.prompt.user_prompt
            )
        )

        return state
    
    async def stream(self, state: AdvisorState) -> AsyncIterator[AgentStreamEvent]:
        if state.prompt is None:
            return

        request = LLMRequest(
            system_prompt=state.prompt.system_prompt,
            user_prompt=state.prompt.user_prompt
        )

        async for event in self._llm_gateway.stream(request):
            if event.type == StreamEventType.COMPLETED.value and event.response is not None:
                state.llm_response = event.response
            
            yield event
