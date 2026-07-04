from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True)
class CategoryAllocation:
    current_value: Decimal
    invested_value: Decimal
    gain: Decimal
    allocation_percentage: Decimal