from enum import StrEnum


class SchemeSort(StrEnum):
    RELEVANCE = 'relevance'
    RETURNS = 'returns'
    RATING = 'rating'
    AUM = 'aum'
    EXPENSE_RATIO = 'expense_ratio'