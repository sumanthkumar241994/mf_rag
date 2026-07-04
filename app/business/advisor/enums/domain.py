from enum import StrEnum


class Domain(StrEnum):
    CUSTOMER = "customer"
    PORTFOLIO = "portfolio"
    INVESTMENT = "investment"
    GOAL = "goal"
    DOCUMENT = "document"
    TAX = "tax"
    TRANSACTION = "transaction"
    MARKET = "market"
    ONBOARDING = "onboarding"
    ADVISOR = "advisor"