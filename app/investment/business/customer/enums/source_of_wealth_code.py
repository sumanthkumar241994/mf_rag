from enum import StrEnum


class SourceOfWealthCode(StrEnum):
    SALARY = "1"
    BUSINESS_INCOME = "2"
    GIFT = "03"
    ANCESTRAL_PROPERTY = "04"
    RENTAL_INCOME = "05"
    PRIZE_MONEY = "06"
    ROYALTY = "07"
    OTHERS = "08"