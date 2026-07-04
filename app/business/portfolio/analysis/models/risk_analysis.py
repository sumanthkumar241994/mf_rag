from dataclasses import dataclass
from decimal import Decimal

@dataclass(slots=True)
class RiskContributor:
    scheme_code: str
    scheme_name: str
    category: str
    allocation_percentage: Decimal
    riskometer: int
    riskometer_display: str
    portfolio_risk_contribution: Decimal

@dataclass(slots=True)
class RiskAnalysis:
    score: int
    portfolio_risk_rating: str
    weighted_risk_score: Decimal
    equity_allocation: Decimal
    debt_allocation: Decimal
    hybrid_allocation: Decimal
    solution_allocation: Decimal
    others_allocation: Decimal
    highest_risk_contributor: RiskContributor | None