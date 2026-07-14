from app.dtos.llm.llm_response import LLMResponse
from app.workflows.advisor.advisor_state import AdvisorState


class ToolFailureNode:
    """
    Builds a user-friendly response when one or more required
    tools fail during execution.
    """

    async def __call__(
        self,
        state: AdvisorState,
    ) -> AdvisorState:

        state.llm_response = LLMResponse(
            answer=self._build_answer(state)
        )

        return state

    def _build_answer(
        self,
        state: AdvisorState,
    ) -> str:

        if not state.errors:
            return (
                "I'm unable to process your request right now. "
                "Please try again later."
            )

        error = state.errors[0]

        if error.retryable:
            return (
                f"{error.message} "
                "Please try again in a few minutes."
            )

        return (
            f"{error.message} "
            "I'm unable to process the request right now."
        )