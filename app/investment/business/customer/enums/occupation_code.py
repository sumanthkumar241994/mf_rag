from enum import StrEnum


class OccupationCode(StrEnum):
    BUSINESS = "01"
    SERVICE = "02"
    PROFESSIONAL = "03"
    AGRICULTURIST = "04"
    RETIRED = "05"
    HOUSEWIFE = "06"
    STUDENT = "07"
    OTHERS = "08"
    DOCTOR = "09"
    PRIVATE_SECTOR_SERVICE = "41"
    PUBLIC_SECTOR_SERVICE = "42"
    FOREX_DEALER = "43"
    GOVERNMENT_SERVICE = "44"
    UNKNOWN = "99"