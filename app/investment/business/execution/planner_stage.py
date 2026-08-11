from typing import Protocol

from app.investment.models.action_type import NextAction
from app.investment.workflows.investment_state import InvestmentState



class PlannerStage(Protocol):

    async def plan(
        self,
        state: InvestmentState,
    ) -> NextAction | None:
        """
        Returns the next action if this stage requires work.
        Returns None if this stage is already satisfied.
        """
        ...