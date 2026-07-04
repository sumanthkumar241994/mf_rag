from dataclasses import dataclass
from datetime import datetime

from app.business.approval.enums.approval_decision import ApprovalDecision


@dataclass(slots=True)
class ApprovalContext:
    decision: ApprovalDecision = ApprovalDecision.AUTO.value
    reason: str | None = None
    reviewer: str | None = None
    comments: str | None = None
    approved_at: datetime | None = None