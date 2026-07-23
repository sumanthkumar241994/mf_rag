from datetime import datetime
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class FeedbackOccurrenceModel(Base):
    __tablename__ = "feedback_occurrences"

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    issue_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("feedback_issues.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    feedback_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("feedback.id", ondelete="CASCADE"),
        nullable=False,
        unique=True,
    )

    conversation_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("conversations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    message_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("messages.id", ondelete="CASCADE"),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
    )