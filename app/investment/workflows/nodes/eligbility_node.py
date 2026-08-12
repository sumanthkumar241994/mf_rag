from __future__ import annotations

from typing import Any

from langgraph.types import interrupt

from app.investment.business.execution.execution_engine import ExecutionEngine
from app.investment.workflows.investment_state import InvestmentState


class EligibilityNode:
    """
    LangGraph node responsible for evaluating customer eligibility
    before proceeding with the investment workflow.

    Responsibilities:
    - Evaluate customer eligibility
    - Populate pending customer actions
    - Interrupt workflow when customer action is required
    - Resume without re-running eligibility
    - Pass the customer's resume selection to the next node

    pending_actions:
        All outstanding customer requirements.

    pending_action:
        The currently selected requirement. This is populated
        later by DataCollectionNode.

    next_action:
        The next workflow action. This is managed separately.
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
        return state

    # async def __call__(
    # self,
    # state: InvestmentState,
    # ) -> InvestmentState:

    #     execution = state.workflow_execution

    #     # ---------------------------------------------------------
    #     # Existing workflow interrupt
    #     #
    #     # This means the eligibility node already executed and
    #     # created the pending-action summary.
    #     #
    #     # DO NOT execute eligibility again.
    #     # ---------------------------------------------------------
    #     if execution is not None and execution.interrupted and execution.interrupt is not None:
    #         resume_data = interrupt(execution.interrupt.to_dict())

    #         state.workflow_resume = resume_data

    #         return state

    #     # First execution
    #     await self._engine.execute(state)

    #     execution = state.workflow_execution

    #     if execution is not None and execution.interrupted and execution.interrupt is not None:
        
    #         interrupt(
    #             execution.interrupt.to_dict()
    #         )

    #     return state