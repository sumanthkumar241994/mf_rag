from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from app.business.customer.enums.gender import Gender
from app.business.customer.enums.marital_status import MaritalStatus


@dataclass(slots=True)
class CustomerProfile:
    customer_id: str
    name: str | None = None
    mobile: str | None = None
    email: str | None = None
    date_of_birth: date | None = None
    age: int | None = None
    gender: Gender = Gender.UNKNOWN
    marital_status: MaritalStatus = MaritalStatus.UNKNOWN
    is_nri: bool = False