from app.core.enums.base_enum import BaseEnum


class KYCStatus(BaseEnum):
    SUBMITTED = "01"
    VERIFIED = "02"
    REJECTED = "04"
    NOT_PRESENT = "05"
    BLOCKED = "06"
    VALIDATED = "07"
    UNKNOWN = "UNKNOWN"

    @property
    def display_name(self) -> str:
        return {
            self.SUBMITTED: "Submitted",
            self.VERIFIED: "Verified",
            self.REJECTED: "Rejected",
            self.NOT_PRESENT: "Not Present",
            self.BLOCKED: "Blocked",
            self.VALIDATED: "Validated",
            self.UNKNOWN: "Unknown",
        }[self]

    @property
    def description(self) -> str:
        return {
            self.SUBMITTED: "Your KYC verification is under review.",
            self.VERIFIED: "Your KYC has been verified.",
            self.REJECTED: "Your KYC verification was rejected.",
            self.NOT_PRESENT: "No KYC record exists for your account.",
            self.BLOCKED: "Your KYC is currently blocked.",
            self.VALIDATED: "Your KYC is validated and you're eligible to invest.",
            self.UNKNOWN: "Your KYC status is unavailable.",
        }[self]

    @property
    def is_completed(self) -> bool:
        return self in (
            self.VALIDATED,
        )   