from enum import StrEnum


class EligibilityRequirementType(StrEnum):
    BANK = "bank"
    NOMINEE = "nominee"
    FATCA = "fatca"
    KYC = "kyc"
    SIGNATURE = "signature"
    ADDRESS = "address"
    EMAIL = "email"