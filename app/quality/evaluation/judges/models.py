from dataclasses import dataclass, field

from pydantic import BaseModel

from app.quality.evaluation.enums import MetricStatus
from app.quality.evaluation.models.judge_models import JudgeIssue


@dataclass(slots=True)
class PlannerCriterion:
    name: str
    score: float
    explanation: str


class PlannerJudgeResponse(BaseModel):
    overall_score: float
    status: MetricStatus
    explanation: str

    criteria: list[PlannerCriterion] = field(default_factory=list)
    issues: list[JudgeIssue] = field(default_factory=list)