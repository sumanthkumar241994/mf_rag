from typing import Any
from pydantic import BaseModel, ConfigDict, Field

from app.investment.business.otp.enums.verification_purpose import VerificationPurpose
from app.investment.common.enums.action_type import ActionType


class VerificationState(BaseModel):
    model_config = ConfigDict(
        use_enum_values=False,
    )

    required: bool = False
    verified: bool = False
    otp_sent: bool = False

    verification_id: str | None = None

    action: ActionType | None = None
    purpose: VerificationPurpose | None = None

    payload: dict[str, Any] = Field(
        default_factory=dict,
    )