from dataclasses import dataclass
from decimal import Decimal

from app.business.goal.enums.goal_type import GoalType


@dataclass(slots=True)
class GoalParameters:
    goal_type: GoalType
    goal_amount : Decimal | None = None
    target_years: int | None = None

    current_corpus: Decimal | None = None
    monthly_investment: Decimal | None = None

    expected_return: Decimal | None = None
    inflation_rate: Decimal | None = None

    current_age: int | None = None
    retirement_age: int | None = None
    target_years: int | None = None