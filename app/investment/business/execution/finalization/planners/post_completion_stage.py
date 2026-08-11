from app.investment.common.enums.action_type import ActionType
from app.investment.models.action_type import NextAction
from app.investment.workflows.investment_state import InvestmentState

class PostCompletionStage:

    async def plan(
        self,
        state: InvestmentState,
    ) -> NextAction:

        return NextAction(
            action=ActionType.COMPLETE,
        )