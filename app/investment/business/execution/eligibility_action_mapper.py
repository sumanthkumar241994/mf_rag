from app.investment.common.enums.action_type import ActionType
from app.investment.common.enums.eligibility_requirement_type import EligibilityRequirementType
from app.investment.models.action_type import NextAction
from app.investment.models.eligibility_requirement import EligibilityRequirement


class EligibilityActionMapper:

    _ACTION_MAP = {
        EligibilityRequirementType.NOMINEE: (
            ActionType.UPDATE_NOMINEE
        ),
        EligibilityRequirementType.FATCA: (
            ActionType.UPDATE_FATCA
        ),
    }

    @classmethod
    def map(
        cls,
        requirement: EligibilityRequirement,
    ) -> NextAction:

        action = cls._ACTION_MAP.get(
            requirement.code
        )

        if action is None:
            raise ValueError(
                f"Unsupported eligibility requirement: "
                f"{requirement.code}"
            )

        return NextAction(
            action=action,
            payload=requirement,
            interrupt=True,
        )