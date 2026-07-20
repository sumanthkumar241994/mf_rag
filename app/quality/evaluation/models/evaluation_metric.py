from dataclasses import dataclass, field
from typing import Any

from ..enums import MetricSource, MetricType, MetricStatus


@dataclass(slots=True, kw_only=True)
class EvaluationMetric:
    metric: MetricType
    source: MetricSource
    score: float | None = None
    status:  MetricStatus | None = None
    reason: str |None = None
    metadata: dict[str, Any] = field(default_factory=dict)