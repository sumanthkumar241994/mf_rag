from __future__ import annotations

from typing import TYPE_CHECKING
import uuid
from datetime import datetime

from sqlalchemy import DateTime, Enum, Float, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.quality.evaluation.enums import EvaluationStatus, EvaluationTriggerType

if TYPE_CHECKING:
    from app.models.evaluation_metric import EvaluationMetricModel



class EvaluationModel(Base):
    __tablename__ = "evaluations"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    conversation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("conversations.id"),
        nullable=False,
        index=True,
    )

    message_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("messages.id"),
        nullable=False,
        unique=True,
        index=True,
    )

    trace_id: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
        index=True,
    )

    status: Mapped[EvaluationStatus] = mapped_column(
        Enum(EvaluationStatus),
        nullable=False,
    )

    overall_score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    trigger_type: Mapped[EvaluationTriggerType] = mapped_column(
        Enum(EvaluationTriggerType),
        nullable=False,
    )

    evaluator_version: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )

    metrics: Mapped[list["EvaluationMetricModel"]] = relationship(
        back_populates="evaluation",
        cascade="all, delete-orphan",
        lazy="selectin",
    )