from enum import Enum


class VerificationPurpose(str, Enum):
    CUSTOMER_UPDATE = "customer_update"
    INVESTMENT = "investment"