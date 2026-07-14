from app.business.advisor.planner.planner import Planner
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

    def __init__(
        self,
        planner: Planner,
    ):
        self._planner = planner

    async def __call__(
        self,
        state: AdvisorState,
    ) -> AdvisorState:

        state.planner_result = await self._planner.plan(state)

        return state