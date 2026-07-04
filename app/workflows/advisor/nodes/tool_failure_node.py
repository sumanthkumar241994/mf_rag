from typing import AsyncIterator
from app.dtos.agents.stream_event import AgentStreamEvent
from app.dtos.llm.llm_response import LLMResponse
from app.enums.stream_event_type import StreamEventType
from app.workflows.advisor.advisor_state import AdvisorState


class ToolFailureNode:
    async def __call__(self, state: AdvisorState) -> AdvisorState:
        state.llm_response = LLMResponse(answer=self._build_answer(state))
        return state
    
    async def stream(self, state: AdvisorState) -> AsyncIterator[AgentStreamEvent]:
        state.llm_response = LLMResponse(answer=self._build_answer(state))

        yield AgentStreamEvent(
            type=StreamEventType.ERROR.value,
            message=state.llm_response.answer
        )

        yield AgentStreamEvent(
            type=StreamEventType.COMPLETED.value,
            response=state.llm_response
        )



    def _build_answer(self, state: AdvisorState) -> str:
        if not state.errors:
            return (
                "I'm unable to process your request right now. "
                "Please try again later."
            )

        error = state.errors[0]

        answer = error.message

        if error.retryable:
            answer += " Please try again in a few minutes."
        else:
            answer += " I'm unable to process the request right now."

        return answer