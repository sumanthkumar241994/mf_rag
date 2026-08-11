from langgraph.types import interrupt
from app.investment.business.execution.execution_engine import ExecutionEngine
from app.investment.workflows.investment_state import InvestmentState


class EligibilityNode:
    """
    LangGraph node responsible for evaluating customer eligibility
    before proceeding with the investment workflow.

    Responsibilities:
    - Evaluate customer eligibility
    - Generate eligibility summary
    - Interrupt workflow when customer action is required
    - Continue when customer is eligible
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

        if state.workflow_execution and state.workflow_execution.interrupted:
            interrupt(
                state.workflow_execution.interrupt.to_dict()
            )

        return state