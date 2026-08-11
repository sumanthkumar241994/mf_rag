from typing import Protocol

from app.investment.models.action_type import NextAction
from app.investment.workflows.investment_state import InvestmentState



class ActionHandler(Protocol):

    async def execute(
        self,
        state: InvestmentState,
        action: NextAction,
    ) -> None:
        pass