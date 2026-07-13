from enum import StrEnum


class GoalParameter(StrEnum):
    GOAL_AMOUNT = "goal_amount"
    TARGET_YEARS = "target_years"
    CURRENT_CORPUS = "current_corpus"
    MONTHLY_INVESTMENT = "monthly_investment"
    EXPECTED_RETURN = "expected_return"
    INFLATION_RATE = "inflation_rate"
    CURRENT_AGE = "current_age"
    RETIREMENT_AGE = "retirement_age"
    ANNUAL_INCOME = "annual_income"
    MONTHLY_EXPENSES = "monthly_expenses"