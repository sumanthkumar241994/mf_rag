from app.investment.business.execution.action_registry import ActionHandlerRegistry
from app.investment.business.execution.planner.execution_planner import ExecutionPlanner
from app.investment.models.execution_result import ExecutionResult, ExecutionStatus
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

            result: ExecutionResult = await handler.execute(
                state=state,
                action=next_action,
            )

            if len(state.errors) > error_count:
                return None

            if result.status == ExecutionStatus.COMPLETED:
                return state.workflow_execution
        