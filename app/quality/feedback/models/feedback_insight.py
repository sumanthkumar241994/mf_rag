from dataclasses import dataclass
from uuid import UUID

from app.notifications.models import NotificationSeverity
from app.quality.feedback.enums.insight import IssueCategory, RootCause



@dataclass(slots=True, kw_only=True)
class FeedbackInsight:
    feedback_id: UUID

    category: IssueCategory
    root_cause: RootCause

    severity: NotificationSeverity
    confidence: float

    summary: str
    recommendation: str