from app.dtos.llm.llm_request import LLMRequest
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