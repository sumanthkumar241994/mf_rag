from app.investment.business.execution.planner_stage import PlannerStage
from app.investment.models.action_type import NextAction
from app.investment.common.enums.action_type import ActionType
from app.investment.workflows.investment_state import InvestmentState


class CustomerActionStage(PlannerStage):

    async def plan(
        self,
        state: InvestmentState,
    ) -> NextAction | None:

        # Resume pending customer action.
        if state.execution_goal is not None:
            return NextAction(
                action=state.execution_goal.operation.action_type,
                payload=state.execution_goal.model_dump(),
            )

        return None