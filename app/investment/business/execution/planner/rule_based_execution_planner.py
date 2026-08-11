

from app.investment.business.execution.planner.execution_planner import ExecutionPlanner
from app.investment.business.execution.planner_stage import PlannerStage
from app.investment.common.enums.action_type import ActionType
from app.investment.models.action_type import NextAction
from app.investment.workflows.investment_state import InvestmentState


class RuleBasedExecutionPlanner(ExecutionPlanner):

    def __init__(
        self,
        stages: list[PlannerStage],
    ):
        self._stages = stages

    async def plan(
        self,
        state: InvestmentState,
    ) -> NextAction:

        for stage in self._stages:

            action = await stage.plan(state)

            if action is not None:
                return action

        # return NextAction(
        #     action=ActionType.COMPLETE,
        # )