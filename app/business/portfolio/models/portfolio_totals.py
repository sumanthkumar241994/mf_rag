from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True)
class PortfolioTotals:
    current_value: Decimal
    net_investment: Decimal
    net_gain: Decimal
    return_percentage: Decimal
    folio_count: int
    holding_count: int
    scheme_count: int
    amc_count: int