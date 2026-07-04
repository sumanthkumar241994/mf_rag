from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True)
class InvestmentTypeAllocation:
    current_value: Decimal
    invested_value: Decimal
    gain: Decimal
    allocation_percentage: Decimal