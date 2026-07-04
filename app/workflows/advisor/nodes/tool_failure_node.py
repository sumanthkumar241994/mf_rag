from app.dtos.llm.llm_response import LLMResponse
from app.workflows.advisor.advisor_state import AdvisorState


class ToolFailureNode:
    async def __call__(self, state: AdvisorState) -> AdvisorState:
        if state.errors:
            error = state.errors[0]
            answer = error.message

            if error.retryable:
                answer += "Please try again in a few minutes"
            else:
                answer += "\n I'm unable to process the request right now"

            state.llm_response = LLMResponse(answer=answer)

            return state