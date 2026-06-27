from __future__ import annotations
import typing
import uuid
from datetime import datetime

from sqlalchemy import Integer, String, DateTime, Enum, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from sqlalchemy import UniqueConstraint, Index

from app.models.base import Base
from app.enums.conversation import MessageRole

if typing.TYPE_CHECKING:
    from app.models.conversation import Conversation

class Message(Base):
    __tablename__ = 'messages'

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    conversation_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("conversations.id", ondelete="CASCADE"), nullable=False, index=True)
    sequence_number: Mapped[int] = mapped_column(Integer, nullable=False)
    role: Mapped[MessageRole] = mapped_column(Enum(MessageRole), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    metadata_: Mapped[dict] = mapped_column("metadata", JSONB, default=dict, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    conversation: Mapped["Conversation"] = relationship("Conversation", back_populates="messages")
    
    __table_args__ = (
        UniqueConstraint(
            "conversation_id",
            "sequence_number",
            name='uq_message_sequence'
        ),
        Index(
            "idx_message_conversation_sequence",
            "conversation_id",
            "sequence_number"
        )
    )