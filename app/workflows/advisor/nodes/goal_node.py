from langgraph.types import interrupt

from app.mapper.advisor_state_mapper import AdvisorStateMapper
from app.tools.implementations.goal_tool import GoalTool
from app.workflows.advisor.advisor_state import AdvisorState


class GoalNode:
    """
    Executes goal analysis and pauses the workflow if additional
    user input is required.
    """

    def __init__(
        self,
        goal_tool: GoalTool,
    ):
        self._goal_tool = goal_tool

    async def __call__(
        self,
        state: AdvisorState,
    ) -> AdvisorState:

        # After resume, LangGraph restores nested objects as dicts.
        # Convert them back into domain models before executing business logic.
        state = AdvisorStateMapper.from_dict(state)

        execution = await self._goal_tool.execute(state)

        state.workflow_execution = execution

        if execution.interrupted:
            state.workflow_interrupt = execution.interrupt
            interrupt(execution.interrupt)

        state.workflow_interrupt = None

        return state