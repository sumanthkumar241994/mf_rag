from dataclasses import dataclass, field
from typing import Any

from ..enums import MetricSource, MetricType, MetricStatus


@dataclass(slots=True, kw_only=True)
class EvaluationMetric:
    type: MetricType
    source: MetricSource
    status: MetricStatus
    score: float | None = None
    explanation: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)