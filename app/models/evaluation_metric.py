from __future__ import annotations

import uuid
from datetime import datetime
from typing import TYPE_CHECKING, Any

from sqlalchemy import DateTime, Enum, Float, ForeignKey, String, func
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base
from app.quality.evaluation.enums import (
    MetricSource,
    MetricStatus,
    MetricType,
)

if TYPE_CHECKING:
    from app.models.evaluation import EvaluationModel


class EvaluationMetricModel(Base):
    __tablename__ = "evaluation_metrics"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    evaluation_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("evaluations.id", ondelete="CASCADE"),
        nullable=False,
        index=True,
    )

    metric: Mapped[MetricType] = mapped_column(
        Enum(MetricType),
        nullable=False,
    )

    source: Mapped[MetricSource] = mapped_column(
        Enum(MetricSource),
        nullable=False,
    )

    status: Mapped[MetricStatus] = mapped_column(
        Enum(MetricStatus),
        nullable=False,
    )

    score: Mapped[float | None] = mapped_column(
        Float,
        nullable=True,
    )

    reason: Mapped[str | None] = mapped_column(
        String,
        nullable=True,
    )

    metadata: Mapped[dict[str, Any]] = mapped_column(
        JSONB,
        nullable=False,
        default=dict,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    evaluation: Mapped["EvaluationModel"] = relationship(
        back_populates="metrics",
    )