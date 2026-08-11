from app.investment.business.execution.planner_stage import PlannerStage
from app.investment.common.enums.action_type import ActionType
from app.investment.models.action_type import NextAction
from app.investment.workflows.investment_state import InvestmentState


class CompletionStage(PlannerStage):
    """
    Final stage of an execution planner.

    Always returns the COMPLETE action so the
    CompletionActionHandler can finalize the current node.
    """

    async def evaluate(
        self,
        state: InvestmentState,
    ) -> NextAction:
        return NextAction(
            action=ActionType.COMPLETE,
        )