

from app.investment.common.enums.action_type import ActionType
from app.investment.common.enums.customer_state import CustomerState
from app.investment.models.action_type import NextAction
from app.investment.workflows.investment_state import InvestmentState


class CustomerSyncStage:

    async def plan(
        self,
        state: InvestmentState,
    ) -> NextAction | None:

        if state.customer_state in (
            CustomerState.NOT_LOADED,
            CustomerState.STALE,
        ):
            return NextAction(
                action=ActionType.CHECK_CUSTOMER,
            )

        return None