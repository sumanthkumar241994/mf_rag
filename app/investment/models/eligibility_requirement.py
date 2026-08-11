from pydantic import Field

from app.investment.base.models import InvestmentBaseModel
from app.investment.common.enums.eligibility_requirement_type import EligibilityRequirementType
from app.investment.common.enums.requirement_status import RequirementStatus


class EligibilityRequirement(InvestmentBaseModel):
    code: EligibilityRequirementType
    status: RequirementStatus
    title: str
    message: str