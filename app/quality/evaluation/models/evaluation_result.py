from dataclasses import dataclass, field

from .evaluation_metric import EvaluationMetric


@dataclass(slots=True, kw_only=True)
class EvaluationResult:
    metrics: list[EvaluationMetric] = field(default_factory=list)
    overall_score: float | None = None