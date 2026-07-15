from __future__ import annotations

import typing
import uuid
from datetime import datetime

from sqlalchemy import (
    DateTime,
    ForeignKey,
    Integer,
    Text,
    String,
    UniqueConstraint,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func

from app.models.base import Base

if typing.TYPE_CHECKING:
    from app.models.conversation import Conversation


class ConversationSummary(Base):
    __tablename__ = "conversation_summaries"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True,default=uuid.uuid4)
    conversation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    start_sequence: Mapped[int] = mapped_column(Integer, nullable=False)
    end_sequence: Mapped[int] = mapped_column(Integer, nullable=False)
    summary: Mapped[str] = mapped_column(Text,nullable=False)
    model: Mapped[str | None] = mapped_column(String(100), nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())
    conversation: Mapped["Conversation"] = relationship("Conversation", back_populates="summaries")

    __table_args__ = (
        UniqueConstraint(
            "conversation_id",
            "version",
            name="uq_conversation_summary_version",
        ),
        Index(
            "idx_conversation_summary_sequence",
            "conversation_id",
            "end_sequence",
        ),
    )