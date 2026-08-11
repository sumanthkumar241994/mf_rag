from pydantic import BaseModel

from app.investment.business.otp.enums.verification_status import VerificationStatus


class VerificationResult(BaseModel):
    success: bool
    status: VerificationStatus
    verification_id: str | None = None
    message: str | None = None