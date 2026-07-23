from app.observability.tracing import trace_step
from app.tools.executor.tool_execution_engine import ToolExecutionEngine
from app.workflows.advisor.advisor_state import AdvisorState


class ToolExecutionNode:
    """
    Executes all tools selected by the planner.
    Each tool enriches the shared AdvisorState.
    """

    def __init__(
        self,
        execution_engine: ToolExecutionEngine,
    ):
        self._execution_engine = execution_engine

    async def __call__(
        self,
        state: AdvisorState,
    ) -> AdvisorState:

        planner_result = state.planner_result

        if planner_result is None:
            return state

        for tool in planner_result.selected_tools:

            response = await self._execution_engine.execute(
                tool_name=tool,
                state=state,
            )

            if not response.success:
                break

            if state.workflow_execution is not None and state.workflow_execution.interrupt is not None:
                break

        return state