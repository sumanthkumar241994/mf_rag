from dataclasses import dataclass, field
from typing import Any

from app.quality.evaluation.enums import MetricStatus


@dataclass(slots=True)
class JudgeIssue:
    code: str
    message: str


@dataclass(slots=True)
class JudgeResult:
    score: float
    status: MetricStatus
    explanation: str
    issues: list[JudgeIssue] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)