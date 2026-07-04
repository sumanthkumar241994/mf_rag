from dataclasses import dataclass
from decimal import Decimal

@dataclass(slots=True)
class DiversificationAnalysis:
    score: int
    diversification_rating: str
    holding_count: int
    amc_count: int
    folio_count: int
    scheme_count: int
    largest_holding_percentage: Decimal
    highest_amc_percentage: Decimal
    is_well_diversified: bool