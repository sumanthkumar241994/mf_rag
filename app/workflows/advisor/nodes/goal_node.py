from langgraph.types import interrupt

from app.tools.implementations.goal_tool import GoalTool
from app.workflows.advisor.advisor_state import AdvisorState


class GoalNode:
    def __init__(self, goal_tool: GoalTool):
        self._goal_tool = goal_tool

    async def __call__(self, state: AdvisorState) -> AdvisorState:
        execution = await self._goal_tool.execute(state)

        if execution.interrupted:
            state.workflow_interrupt = execution.interrupt

            interrupt(execution.interrupt)
        
        state.workflow_interrupt = None
        
        return state