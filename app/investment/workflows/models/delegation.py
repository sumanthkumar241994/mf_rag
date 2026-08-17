from typing import Any
from pydantic import BaseModel, Field

from app.enums.delegation_reason import DelegationReason
from app.enums.workflow import WorkflowType


class Delegation(BaseModel):
    source: WorkflowType
    target: WorkflowType
    reason: DelegationReason
    payload: dict[str, Any] = Field(
        default_factory=dict,
    )