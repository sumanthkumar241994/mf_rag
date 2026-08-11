from decimal import Decimal
from pydantic import BaseModel

class SchemeAllocation(BaseModel):
    scheme_id: int
    allocation_percent: Decimal = Decimal("100")
    target_roi: Decimal = Decimal("0")
    min_sip_amount: Decimal = Decimal("0")