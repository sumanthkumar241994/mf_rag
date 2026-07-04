from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True)
class PerformanceHolding:
    scheme_code: str
    scheme_name: str
    category: str
    amc_name: str
    one_year_return: Decimal | None = None
    three_year_return: Decimal | None = None
    five_year_return: Decimal | None = None
    performance_score: Decimal | None = None 

@dataclass(slots=True)
class PerformanceAnalysis:
    best_performing_holding: PerformanceHolding | None
    worst_performing_holding: PerformanceHolding | None
    score: Decimal
    performance_rating: str
    average_one_year_return: Decimal
    average_three_year_return: Decimal
    average_five_year_return: Decimal