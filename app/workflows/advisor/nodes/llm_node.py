from app.dtos.llm.llm_request import LLMRequest
from app.llm_gateway.llm_gateway import LLMGateway
from app.workflows.advisor.advisor_state import AdvisorState

from langgraph.config import get_stream_writer

class LLMNode:
    """
    Executes the final LLM generation.
    """
    def __init__(self, gateway: LLMGateway):
        self._gateway = gateway

    
    async def __call__(self, state: AdvisorState):

        writer = get_stream_writer()
        request = LLMRequest(
                system_prompt=state.prompt.system_prompt,
                user_prompt=state.prompt.user_prompt
            )
        async for chunk in self._gateway.astream(request):

            if chunk.token:

                writer(
                    {
                        "type": "token",
                        "token": chunk.token,
                    }
                )

            elif chunk.response:

                state.llm_response = chunk.response

                writer(
                    {
                        "type": "completed",
                        "response": chunk.response
                    }
                )

        return state

    async def generate(self, state):
        request = LLMRequest(
                system_prompt=state.prompt.system_prompt,
                user_prompt=state.prompt.user_prompt
            )

        state.llm_response = await self._gateway.generate(request)

        return state
    
    # async def stream(self, state: AdvisorState) -> AsyncIterator[LLMChunk]:
    #     if state.prompt is None:
    #         return

    #     async for  chunk in self._runnable.astream(state.prompt):
            
    #         if chunk.response:
    #             state.llm_response = chunk.response
            
    #         yield chunk
