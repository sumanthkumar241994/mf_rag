from langgraph.types import interrupt
from app.investment.business.execution.customer.planners.customer_update_stage import OperationActionMapper
from app.investment.business.execution.execution_engine import ExecutionEngine
from app.investment.workflows.investment_state import InvestmentState


class CustomerNode:
    """
    Executes customer-related operations.
    """

    def __init__(
        self,
        engine: ExecutionEngine,
    ) -> None:
        self._engine = engine

    async def __call__(
        self,
        state: InvestmentState,
    ) -> InvestmentState:

        await self._engine.execute(state)

        execution = state.workflow_execution

        # Do not use workflow_execution.interrupted as the
        # generic LangGraph interrupt mechanism here.
        if (
            execution is not None
            and execution.interrupted
            and execution.interrupt is not None
        ):
            interrupt(
                execution.interrupt.model_dump(
                    mode="json"
                )
            )

        # If customer operation completed successfully,
        # finalize the execution goal.
        self._complete_execution_goal(state)

        return state

    @staticmethod
    def _complete_execution_goal(
        state: InvestmentState,
    ) -> None:

        goal = state.execution_goal

        if goal is None:
            return

        completed_action = OperationActionMapper.map(
            goal.operation,
        )

        # Remove the completed action from pending actions.
        state.pending_actions = [
            pending_action
            for pending_action in state.pending_actions
            if pending_action.action != completed_action
        ]

        # The selected pending action is complete.
        if state.pending_actions:
            state.pending_action = state.pending_actions[0]
        else:
            state.pending_action = None

        # The execution goal has been consumed.
        state.execution_goal = None

        # Verification belongs to this execution.
        state.verification = None