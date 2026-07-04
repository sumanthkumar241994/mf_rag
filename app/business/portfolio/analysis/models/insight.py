from dataclasses import dataclass, field
from typing import Any

from app.business.portfolio.analysis.enums.insight_category import InsightCategory
from app.business.portfolio.analysis.enums.insight_code import InsightCode
from app.business.portfolio.analysis.enums.severity import Severity

@dataclass(slots=True)
class Insight:
    code: InsightCode
    category: InsightCategory
    severity: Severity
    title: str
    description: str
    metadata: dict[str, Any] = field(default_factory=dict)