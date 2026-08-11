from app.investment.business.execution.action_registry import ActionHandlerRegistry
from app.investment.business.execution.planner.execution_planner import ExecutionPlanner
from app.investment.workflows.investment_state import (
    InvestmentState,
)
from app.workflows.workflow.models.workflow_execution import (
    WorkflowExecution,
)


class ExecutionEngine:

    def __init__(
        self,
        planner: ExecutionPlanner,
        action_handler_registry: ActionHandlerRegistry,
    ):
        self._planner = planner
        self._action_handler_registry = (
            action_handler_registry
        )

    async def execute(
        self,
        state: InvestmentState,
    ) -> WorkflowExecution | None:

        while True:
            next_action = await self._planner.plan(state)
            if next_action is None:
                return

            state.next_action = next_action

            handler = (
                self._action_handler_registry.get(
                    next_action.action,
                )
            )

            error_count = len(state.errors)

            await handler.execute(
                state=state,
                action=next_action,
            )

            if len(state.errors) > error_count:
                return None

            # Any interrupt immediately pauses execution.
            if state.workflow_execution and state.workflow_execution.interrupted:
                return state.workflow_execution