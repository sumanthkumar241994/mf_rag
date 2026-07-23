from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, Enum, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base
from app.notifications.models import NotificationSeverity
from app.quality.feedback.enums.insight import FeedbackIssueStatus, IssueCategory, RootCause



class FeedbackIssueModel(Base):
    __tablename__ = "feedback_issues"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    category: Mapped[IssueCategory] = mapped_column(
        Enum(IssueCategory),
        nullable=False,
        index=True,
    )

    root_cause: Mapped[RootCause] = mapped_column(
        Enum(RootCause),
        nullable=False,
        index=True,
    )

    severity: Mapped[NotificationSeverity] = mapped_column(
        Enum(NotificationSeverity),
        nullable=False,
    )

    jira_key: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
    )

    jira_url: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
    )

    occurrence_count: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        default=1,
    )

    status: Mapped[FeedbackIssueStatus] = mapped_column(
        Enum(FeedbackIssueStatus),
        nullable=False,
        default=FeedbackIssueStatus.OPEN,
        index=True,
    )

    first_seen: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    last_seen: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )