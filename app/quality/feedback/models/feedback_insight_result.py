from pydantic import BaseModel

from app.notifications.models import NotificationSeverity
from app.quality.feedback.enums.insight import IssueCategory, RootCause


class FeedbackInsightResult(BaseModel):
    category: IssueCategory
    root_cause: RootCause
    severity: NotificationSeverity
    confidence: float
    summary: str
    recommendation: str