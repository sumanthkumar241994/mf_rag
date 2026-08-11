from typing import Any

from pydantic import BaseModel, Field

from app.investment.business.otp.enums.verification_purpose import VerificationPurpose
from app.investment.common.enums.action_type import ActionType


class VerificationRequest(BaseModel):
    customer_id: str
    action: ActionType
    purpose: VerificationPurpose

    payload: dict[str, Any] = Field(
        default_factory=dict,
    )