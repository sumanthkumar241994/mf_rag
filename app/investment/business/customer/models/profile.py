from datetime import date

from app.investment.base.models import InvestmentBaseModel
from app.investment.business.customer.enums.gender import Gender
from app.investment.business.customer.enums.marital_status import MaritalStatus
from pydantic import computed_field


class CustomerProfile(InvestmentBaseModel):
    customer_id: str
    name: str | None = None
    mobile: str | None = None
    email: str | None = None
    date_of_birth: date | None = None
    gender: Gender = Gender.UNKNOWN
    marital_status: MaritalStatus = MaritalStatus.UNKNOWN
    is_nri: bool = False

    @computed_field
    @property
    def age(self) -> int | None:
        if self.date_of_birth is None:
            return None

        today = date.today()
        return (
            today.year
            - self.date_of_birth.year
            - (
                (today.month, today.day)
                < (self.date_of_birth.month, self.date_of_birth.day)
            )
        )