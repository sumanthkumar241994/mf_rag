from dataclasses import dataclass, field

from app.business.advisor.planner.models.planner_error import PlannerError
from app.business.advisor.planner.models.planner_response import PlannerResponse


@dataclass
class PlannerValidationResult:
    valid: bool
    response: PlannerResponse | None = None
    errors: list[PlannerError] = field(default_factory=list)