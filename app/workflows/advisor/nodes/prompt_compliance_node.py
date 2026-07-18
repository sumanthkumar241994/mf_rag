from app.compliance.prompt.models.prompt_compliance_request import (
    PromptComplianceRequest,
)
from app.compliance.prompt.prompt_compliance_service import PromptComplianceService
from app.dtos.llm.llm_response import LLMResponse
from app.workflows.advisor.advisor_state import AdvisorState


class PromptComplianceNode:

    def __init__(
        self,
        prompt_compliance_service: PromptComplianceService,
    ):
        self._prompt_compliance_service = prompt_compliance_service

    async def __call__(
        self,
        state: AdvisorState,
    ) -> AdvisorState:

        result = await self._prompt_compliance_service.validate(
            PromptComplianceRequest(
                prompt=state.prompt,
            )
        )

        state.prompt_compliance_result = result

        if not result.allowed:

            state.llm_response = LLMResponse(
                answer=(
                    "I'm unable to process this request because it "
                    "doesn't meet our compliance requirements. "
                    "Please rephrase your request or contact "
                    "support if you need assistance."
                )
            )

            return state

        state.prompt = result.sanitized_prompt

        return state