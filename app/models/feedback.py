from datetime import datetime
from uuid import uuid4

from sqlalchemy import (
    DateTime,
    Enum,
    ForeignKey,
    String,
    func,
    Text,
    UniqueConstraint,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base
from app.quality.feedback.enums.feedback_reason import FeedbackReason
from app.quality.feedback.enums.feedback_signal import FeedbackSignal



class Feedback(Base):
    __tablename__ = "feedback"

    __table_args__ = (
        UniqueConstraint(
            "customer_id",
            "message_id",
            name="uq_feedback_customer_message",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    customer_id: Mapped[str] = mapped_column(
        String(12),
        nullable=False,
        index=True,
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
        index=True,
    )

    trace_id: Mapped[UUID | None] = mapped_column(
        UUID(as_uuid=True),
        nullable=True,
        index=True,
    )

    signal: Mapped[FeedbackSignal] = mapped_column(
        Enum(FeedbackSignal, name="feedback_signal"),
        nullable=False,
    )

    reason: Mapped[FeedbackReason | None] = mapped_column(
        Enum(FeedbackReason, name="feedback_reason"),
        nullable=True,
    )

    comment: Mapped[str | None] = mapped_column(
        Text,
        nullable=True,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(), 
        onupdate=func.now()
    )