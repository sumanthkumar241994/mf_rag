from pydantic import BaseModel
from datetime import date


class SipDetails(BaseModel):
    instalment_period: str
    instalment_count: int
    sip_day: int
    start_date: date
    first_payment: bool = True
    bank_account_id: int | None = None