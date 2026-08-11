from app.investment.common.enums.action_type import ActionType
from app.investment.common.enums.eligibility_requirement_type import (
    EligibilityRequirementType,
)
from app.investment.models.action_type import NextAction
from app.investment.services.eligibility_service import EligibilityService
from app.investment.workflows.investment_state import InvestmentState


class EligibilityStage:

    def __init__(
        self,
        eligibility_service: EligibilityService,
    ):
        self._eligibility_service = eligibility_service

    async def plan(
        self,
        state: InvestmentState,
    ) -> NextAction | None:

        eligibility = self._eligibility_service.evaluate(
            state.customer,
        )

        state.eligibility = eligibility

        if eligibility.eligible:
            return None

        return NextAction(
            action=ActionType.REQUEST_DATA_COLLECTION,
            payload=eligibility,
        )

        # requirement = eligibility.required[0] if eligibility.required else None

        # if requirement is None:
        #     return NextAction(
        #         action=ActionType.WAIT_FOR_APPROVAL,
        #         payload=eligibility,
        #     )

        # action_map = {
        #     EligibilityRequirementType.BANK: ActionType.UPDATE_BANK,
        #     EligibilityRequirementType.NOMINEE: ActionType.UPDATE_NOMINEE,
        #     EligibilityRequirementType.FATCA: ActionType.UPDATE_FATCA,
        #     EligibilityRequirementType.KYC: ActionType.COMPLETE_KYC,
        #     EligibilityRequirementType.SIGNATURE: ActionType.UPDATE_SIGNATURE,
        # }

        # return NextAction(
        #     action=action_map[requirement.code],
        #     payload=eligibility,
        # )