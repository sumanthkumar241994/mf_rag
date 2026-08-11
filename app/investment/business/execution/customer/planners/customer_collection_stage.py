from app.investment.business.execution.planner_stage import (
    PlannerStage,
)
from app.investment.common.enums.action_type import (
    ActionType,
)
from app.investment.common.enums.eligibility_requirement_type import (
    EligibilityRequirementType,
)
from app.investment.models.action_type import (
    NextAction,
)
from app.investment.workflows.investment_state import (
    InvestmentState,
)


class CustomerCollectionStage(PlannerStage):

    async def plan(
        self,
        state: InvestmentState,
    ) -> NextAction | None:

        #
        # Already executing an update.
        #
        if state.execution_goal is not None:
            return None

        eligibility = state.eligibility

        if (
            eligibility is None
            or eligibility.eligible
        ):
            return None

        requirement = (
            eligibility.required[0]
            if eligibility.required
            else None
        )

        if requirement is None:
            return None

        action_map = {
            EligibilityRequirementType.NOMINEE: (
                ActionType.COLLECT_NOMINEE
            ),
            EligibilityRequirementType.FATCA: (
                ActionType.COLLECT_FATCA
            ),
        }

        action = action_map.get(
            requirement.code,
        )

        if action is None:
            return None

        return NextAction(
            action=action,
            payload=requirement.model_dump(),
        )