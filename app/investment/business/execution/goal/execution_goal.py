from pydantic import BaseModel

from app.investment.business.otp.enums.verification_purpose import VerificationPurpose
from app.investment.common.enums.operation_type import OperationType



class ExecutionGoal(BaseModel):
    operation: OperationType
    verification_purpose: VerificationPurpose | None = None

    @property
    def requires_verification(self) -> bool:
        return False