from app.business.goal.enums.goal_type import GoalType
from app.business.goal.models.goal import Goal
from app.business.goal.models.goal_parameters import GoalParameters
from app.business.goal.utils import extract_amount, extract_expected_return, extract_inflation_rate, extract_retirement_age, extract_target_years, extract_years, normalize_query


class GoalParser:
    def parse(self, goal_type: GoalType, query: str) -> tuple[Goal, GoalParameters]:
        query = normalize_query(query)

        return (
            Goal(
                goal_type=goal_type,
                title=goal_type.value
            ),

            GoalParameters(
            goal_type=goal_type,
            goal_amount=extract_amount(query),
            target_years=extract_target_years(query),
            retirement_age=extract_retirement_age(query),
            expected_return=extract_expected_return(query),
            inflation_rate=extract_inflation_rate(query)
        )
        )