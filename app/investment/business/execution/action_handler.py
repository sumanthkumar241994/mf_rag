from typing import Protocol

from app.investment.models.action_type import NextAction
from app.investment.models.execution_result import ExecutionResult
from app.investment.workflows.investment_state import InvestmentState



class ActionHandler(Protocol):

    async def execute(
        self,
        state: InvestmentState,
        action: NextAction,
    ) -> ExecutionResult:
        pass