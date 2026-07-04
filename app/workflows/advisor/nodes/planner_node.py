from typing import AsyncIterator
from app.business.advisor.models import planner_result
from app.business.advisor.planner.planner import Planner
from app.dtos.agents.stream_event import AgentStreamEvent
from app.enums.stream_event_type import StreamEventType
from app.workflows.advisor.advisor_state import AdvisorState


class PlannerNode:
    """
    LangGraph node responsible for planning the request.

    Determines:
    - Intent
    - Capabilities
    - Agent
    - Tools
    """
    def __init__(self,planner: Planner):
        self._planner = planner

    async def __call__(self, state: AdvisorState) -> AdvisorState:
        planner_result = await self._planner.plan(state)

        state.planner_result = planner_result

        return state

    async def stream(self, state: AdvisorState) -> AsyncIterator[AgentStreamEvent]:
        """
        Streaming version of the planner.
        Emits planner lifecycle events while updating the shared state.
        """
        yield AgentStreamEvent(type=StreamEventType.PLANNER_START.value)

        state.planner_result = await self._planner.plan(state)

        yield AgentStreamEvent(
            type=StreamEventType.PLANNER_END.value,
            metadata = {
                "intent": state.planner_result.intent.value,
                "tools": [tool.value for tool in state.planner_result.selected_tools],
                "confidence": state.planner_result.confidence
            }
        )

