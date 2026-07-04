
from dataclasses import dataclass, field
from typing import Any

from app.business.portfolio.analysis.enums.recommendation_code import RecommendationCode
from app.business.portfolio.analysis.enums.recommendation_priority import RecommendationPriority


@dataclass(slots=True)
class Recommendation:
    code: RecommendationCode
    priority: RecommendationPriority
    title: str
    description: str
    rationale: str
    metadata: dict[str, Any] = field(default_factory=dict)