from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True)
class GoalPortfolioSnapshot:
    current_corpus: Decimal
    total_investment: Decimal
    monthly_investment: Decimal
    equity_value: Decimal
    debt_value: Decimal
    hybrid_value: Decimal
