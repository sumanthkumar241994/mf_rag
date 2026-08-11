from langgraph.types import interrupt
from app.investment.business.execution.execution_engine import ExecutionEngine
from app.investment.workflows.investment_state import InvestmentState


class CustomerNode:
    """
    LangGraph node responsible for executing all customer-related
    operations required by the investment workflow.

    Responsibilities:
    - Retrieve customer
    - Register customer
    - Update nominee
    - Update bank
    - Update FATCA
    - Update signature
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

        if state.workflow_execution.interrupted:
            interrupt(
                state.workflow_execution.interrupt.model_dump()
            )

        return state