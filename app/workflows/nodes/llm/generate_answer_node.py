# app/workflows/nodes/llm/generate_answer_node.py

from app.workflows.advisor.advisor_state import AdvisorState

from app.dtos.llm.llm_request import LLMRequest

from app.llm_gateway.llm_gateway import LLMGateway

from app.prompts.system.advisor_system_prompt import ADVISOR_SYSTEM_PROMPT

from app.observability.tracing import trace_step


class GenerateAnswerNode:
    def __init__(self, llm_gateway: LLMGateway):
        self.llm_gateway = llm_gateway
    
    @trace_step("generate_answer")
    async def __call__(
        self,
        state: AdvisorState
    ) -> dict:
        llm_response = await self.llm_gateway.generate(
            request=LLMRequest(
                user_prompt=state['query'],
                system_prompt=ADVISOR_SYSTEM_PROMPT,
                context=state['context']
            )
        )

        return {"answer": llm_response.answer}

    async def stream(self, state: AdvisorState):
        request=LLMRequest(
            user_prompt=state['query'],
            system_prompt=ADVISOR_SYSTEM_PROMPT,
            context=state['context']
        )

        async for token in self.llm_gateway.stream(request):
            yield token