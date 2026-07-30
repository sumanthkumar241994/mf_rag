from datetime import date


from app.investment.base.models import InvestmentBaseModel
from app.investment.business.customer.enums.nominee_identity_type import NomineeIdentityType


class Nominee(InvestmentBaseModel):
    exists: bool = False
    name: str | None = None
    relationship: str | None = None
    date_of_birth: date | None = None
    guardian: str | None = None
    identity_type: NomineeIdentityType = (
        NomineeIdentityType.UNKNOWN
    )