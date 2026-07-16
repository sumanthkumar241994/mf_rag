from app.ai.guardrails.guardrail_service import GuardRailService
from app.dtos.llm.llm_response import LLMResponse
from app.workflows.advisor.advisor_state import AdvisorState


class GuardRailNode:

    def __init__(
        self,
        guardrail_service: GuardRailService,
    ):
        self._guardrail_service = guardrail_service

    async def __call__(
        self,
        state: AdvisorState,
    ) -> AdvisorState:

        result = await self._guardrail_service.validate(
            request_context=state.request,
        )

        state.guardrail_result = result

        if not result.allowed:
            state.llm_response = LLMResponse(
                answer=result.response,
            )

        return state