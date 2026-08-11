from typing import Protocol

from app.investment.business.execution.planner_stage import PlannerStage
from app.investment.models.action_type import NextAction
from app.investment.workflows.investment_state import InvestmentState


class ExecutionPlanner:

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

            if action:
                return action

        raise RuntimeError("No planner stage produced an action.")