from typing import Protocol

from app.investment.workflows.investment_state import InvestmentState
from app.investment.workflows.models.delegation import Delegation


class DelegationBuilder(Protocol):

    def supports(
        self,
        state: InvestmentState,
    ) -> bool:
        ...

    def build(
        self,
        state: InvestmentState,
    ) -> Delegation:
        ...