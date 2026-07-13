from __future__ import annotations

from copy import deepcopy
from collections.abc import Callable

from app.business.goal.enums.goal_parameter import GoalParameter
from app.business.goal.models.goal_analysis import GoalAnalysis
from app.business.goal.models.goal_parameters import GoalParameters
from app.business.goal.utils import (
    extract_current_age,
    extract_expected_return,
    extract_goal_amount,
    extract_inflation_rate,
    extract_monthly_investment,
    extract_resume_age,
    extract_retirement_age,
    extract_target_years,
)


class GoalResumeParser:

    def __init__(self):
        self._extractors: dict[
            GoalParameter,
            Callable[[str], object | None],
        ] = {
            GoalParameter.GOAL_AMOUNT: extract_goal_amount,
            GoalParameter.TARGET_YEARS: extract_target_years,
            GoalParameter.CURRENT_AGE: extract_resume_age,
            GoalParameter.RETIREMENT_AGE: extract_resume_age,
            GoalParameter.MONTHLY_INVESTMENT: extract_monthly_investment,
            GoalParameter.EXPECTED_RETURN: extract_expected_return,
            GoalParameter.INFLATION_RATE: extract_inflation_rate,
        }

        self._parameter_attributes: dict[
            GoalParameter,
            str,
        ] = {
            GoalParameter.GOAL_AMOUNT: "goal_amount",
            GoalParameter.TARGET_YEARS: "target_years",
            GoalParameter.CURRENT_AGE: "current_age",
            GoalParameter.RETIREMENT_AGE: "retirement_age",
            GoalParameter.MONTHLY_INVESTMENT: "monthly_investment",
            GoalParameter.EXPECTED_RETURN: "expected_return",
            GoalParameter.INFLATION_RATE: "inflation_rate",
        }

    def update(
        self,
        parameters: GoalParameters,
        missing_parameters: list[GoalParameter],
        answer: str,
    ) -> GoalParameters:

        for parameter in missing_parameters:

            extractor = self._extractors.get(parameter)

            if extractor is None:
                continue

            attribute = self._parameter_attributes.get(parameter)

            if attribute is None:
                continue

            value = extractor(answer)

            if value is None:
                continue

            setattr(
                parameters,
                attribute,
                value,
            )

        return parameters