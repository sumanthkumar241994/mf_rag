from enum import StrEnum

class SchemeCategory(StrEnum):
    EQUITY = "equity"
    DEBT = "debt"
    HYBRID = "hybrid"
    SOLUTION = "solution"
    OTHERS = "others"


class InvestmentType(StrEnum):
    SIP = "sip"
    LUMPSUM = "lumpsum"


class PerformanceRating(StrEnum):
    EXCELLENT = "excellent"
    GOOD = "good"
    AVERAGE = "average"
    NEEDS_REVIEW = "needs_review"
    UNKNOWN = "unknown"