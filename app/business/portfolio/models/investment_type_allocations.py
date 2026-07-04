from dataclasses import dataclass
from .investment_type_allocation import InvestmentTypeAllocation


@dataclass(slots=True)
class InvestmentTypeAllocations:
    sip: InvestmentTypeAllocation
    lumpsum: InvestmentTypeAllocation