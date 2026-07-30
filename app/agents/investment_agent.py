from typing import AsyncIterator

from app.agents.base_agent import BaseAgent
from app.dtos.agents.agent_response import AgentResponse
from app.dtos.agents.stream_event import AgentStreamEvent
from app.dtos.request_context import RequestContext
from app.enums.workflow import WorkflowType
from app.investment.workflows.investment_state import InvestmentState
from app.investment.workflows.investment_workflow import InvestmentWorkflow


class InvestmentAgent(BaseAgent):

    def __init__(self, investment_workflow: InvestmentWorkflow):
        self._investment_workflow = investment_workflow

    @property
    def workflow_name(self) -> str:
        return WorkflowType.INVESTMENT.value

    def create_state(self, request: RequestContext, history: list, trace_id: str) -> InvestmentState:
        return InvestmentState(
            request=request,
            history=history,
            trace_id=trace_id,
        )

    async def run(self, state: InvestmentState) -> AgentResponse:
        state = await self._investment_workflow.invoke(state)
        return self._build_response(state)

    async def resume(self, state: InvestmentState) -> AgentResponse:
        state = await self._investment_workflow.resume(state)
        return self._build_response(state)

    async def stream(self, state: InvestmentState) -> AsyncIterator[AgentStreamEvent]:
        async for event in self._investment_workflow.stream(state):
            yield event

    async def resume_stream(self, state: InvestmentState) -> AsyncIterator[AgentStreamEvent]:
        async for event in self._investment_workflow.resume_stream(state):
            yield event

    def _build_response(self, state: InvestmentState) -> AgentResponse:

        metadata = dict(state.metadata)

        if state.workflow_execution and state.workflow_execution.interrupted:
            return AgentResponse(
                conversation_id=state.request.conversation_id,
                workflow_interrupt=state.workflow_execution.interrupt,
                metadata=metadata,
            )

        return AgentResponse(
            conversation_id=state.request.conversation_id,
            answer=state.response.message if state.response else "",
            metadata=metadata,
        )