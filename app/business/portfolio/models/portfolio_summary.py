from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True)
class LargestHoldingSummary:
    scheme_name: str
    scheme_code: str
    category: str
    amc_name: str
    current_value: Decimal
    allocation_percentage: Decimal


@dataclass(slots=True)
class PortfolioSummary:
    largest_holding: LargestHoldingSummary | None
    highest_risk_category: str | None
    highest_exposure_amc: str | None
    highest_exposure_amc_percentage: Decimal