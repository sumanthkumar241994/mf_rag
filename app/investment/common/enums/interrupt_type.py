from enum import StrEnum


class InterruptType(StrEnum):
    """
    User actions required before workflow execution can resume.
    """
    COLLECT_DATA = 'collect_data'
    ELIGIBILITY = 'eligibility'

    # Customer onboarding
    BANK_UPDATE = "bank_update"
    NOMINEE_UPDATE = "nominee_update"
    FATCA_UPDATE = "fatca_update"
    KYC_UPDATE = "kyc_update"
    RISK_PROFILE_UPDATE = "risk_profile_update"

    # Transaction authorization
    OTP_VERIFICATION = "otp_verification"

    # Advisor interaction
    ADVISOR_CONFIRMATION = "advisor_confirmation"

    # Generic confirmation
    USER_CONFIRMATION = "user_confirmation"

    # External/manual intervention
    MANUAL_REVIEW = "manual_review"