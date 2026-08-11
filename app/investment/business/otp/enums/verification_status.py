from enum import Enum


class VerificationStatus(str, Enum):
    OTP_SENT = "otp_sent"
    VERIFIED = "verified"
    INVALID = "invalid"
    EXPIRED = "expired"
    MAX_ATTEMPTS = "max_attempts"