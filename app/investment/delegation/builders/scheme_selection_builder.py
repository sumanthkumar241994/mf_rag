from typing import Any

from app.enums.delegation_reason import DelegationReason
from app.enums.workflow import WorkflowType
from app.investment.workflows.investment_state import InvestmentState
from app.investment.workflows.models.delegation import Delegation


class SchemeSelectionDelegationBuilder:
    """
    Builds an Investment -> Advisor delegation when the
    investment workflow requires scheme selection.
    """

    def supports(
        self,
        state: InvestmentState,
    ) -> bool:

        # For now this builder is explicitly used by the
        # scheme-selection delegation route.
        return True

    def build(
        self,
        state: InvestmentState,
    ) -> Delegation:

        return Delegation(
            source=WorkflowType.INVESTMENT_PURCHASE,
            target=WorkflowType.ADVISOR,
            reason=DelegationReason.SCHEME_SELECTION,
            payload=self._build_payload(state),
        )

    @staticmethod
    def _build_payload(
        state: InvestmentState,
    ) -> dict[str, Any]:

        return {
            "query": f"Find the suitable schemes for the question - {state.request.query}",
        }