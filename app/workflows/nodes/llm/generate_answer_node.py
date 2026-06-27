# app/workflows/nodes/llm/generate_answer_node.py

from alembic import context
from sqlalchemy.sql.functions import user
from app.workflows.advisor.advisor_state import AdvisorState

from app.dtos.llm.llm_request import LLMRequest

from app.llm_gateway.llm_gateway import LLMGateway

from app.prompts.advisor.system_prompt import ADVISOR_SYSTEM_PROMPT
from app.prompts.advisor.prompt_builder import AdvisorPromptBuilder
from app.observability.tracing import trace_step


class GenerateAnswerNode:
    def __init__(self, llm_gateway: LLMGateway):
        self.llm_gateway = llm_gateway
        self.prompt_builder = AdvisorPromptBuilder()
    
    @trace_step("generate_answer")
    async def __call__(
        self,
        state: AdvisorState
    ) -> dict:
        user_prompt = self.prompt_builder.build(state)
        llm_response = await self.llm_gateway.generate(
            request=LLMRequest(
                user_prompt=user_prompt,
                system_prompt=ADVISOR_SYSTEM_PROMPT,
            )
        )

        return {
            "answer": llm_response.answer, 
            "llm_usage": llm_response.usage, 
            "llm_metrics": llm_response.metrics
            }

    async def stream(self, state: AdvisorState):
        user_prompt = self.prompt_builder.build(state)
        request=LLMRequest(
            user_prompt=user_prompt,
            system_prompt=ADVISOR_SYSTEM_PROMPT,
        )

        async for event in self.llm_gateway.stream(request):
            yield event