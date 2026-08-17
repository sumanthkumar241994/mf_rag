from app.investment.delegation.builders.delegation_builder import DelegationBuilder
from app.investment.workflows.investment_state import InvestmentState
from app.investment.workflows.models.delegation import Delegation


class DelegationBuilderRegistry:

    def __init__(
        self,
        builders: list[DelegationBuilder],
    ) -> None:
        self._builders = builders

    def get(
        self,
        state: InvestmentState,
    ) -> DelegationBuilder:

        for builder in self._builders:
            if builder.supports(state):
                return builder

        raise ValueError(
            "No delegation builder found for the current "
            "investment workflow state."
        )