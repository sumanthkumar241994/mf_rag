from enum import StrEnum


class AgentType(StrEnum):
    ADVISOR = 'advisor'
    PORTFOLIO = 'portfolio'
    GOAL = 'goal'
    TAX = 'tax'
    TRANSACTION = 'transaction'
    COMPARISION = 'comparision'