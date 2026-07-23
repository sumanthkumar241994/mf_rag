from dataclasses import dataclass, field
from datetime import datetime
from uuid import UUID

from .evaluation_metric import EvaluationMetric
from ..enums import EvaluationStatus


@dataclass(slots=True, kw_only=True)
class Evaluation:
    id: UUID
    conversation_id: UUID
    message_id: UUID
    status: EvaluationStatus
    overall_score: float | None = None
    metrics: list[EvaluationMetric] = field(default_factory=list)
    created_at: datetime | None = None
    updated_at: datetime | None = None