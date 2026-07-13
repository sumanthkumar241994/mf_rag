from dataclasses import dataclass
from decimal import Decimal


@dataclass(slots=True)
class GoalProjection:
    projected_goal_amount: Decimal
    projected_corpus: Decimal
    funding_gap: Decimal
    required_monthly_investment: Decimal
    additional_monthly_investment: Decimal