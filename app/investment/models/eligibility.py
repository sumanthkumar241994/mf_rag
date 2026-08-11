from pydantic import Field

from app.investment.base.models import InvestmentBaseModel
from app.investment.models.eligibility_requirement import EligibilityRequirement


class Eligibility(InvestmentBaseModel):
    eligible: bool = False
    required: list[EligibilityRequirement] = Field(default_factory=list)
    pending: list[EligibilityRequirement] = Field(default_factory=list)