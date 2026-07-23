from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import UUID, uuid4

from app.models.feedback_issue import FeedbackIssueModel
from app.notifications.models import NotificationSeverity
from app.quality.feedback.enums.insight import FeedbackIssueStatus, IssueCategory, RootCause



@dataclass(slots=True, kw_only=True)
class FeedbackIssue:
    id: UUID = field(default_factory=uuid4)

    category: IssueCategory
    root_cause: RootCause

    severity: NotificationSeverity

    jira_key: str | None = None
    jira_url: str | None = None

    status: FeedbackIssueStatus = FeedbackIssueStatus.OPEN

    occurrence_count: int = 1

    first_seen: datetime = field(default_factory=lambda: datetime.now(UTC))
    last_seen: datetime = field(default_factory=lambda: datetime.now(UTC))

    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = field(default_factory=lambda: datetime.now(UTC))