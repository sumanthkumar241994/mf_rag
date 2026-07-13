from dataclasses import dataclass

from app.business.goal.enums.goal_status import GoalStatus
from app.business.goal.models.goal import Goal
from app.business.goal.models.goal_parameters import GoalParameters
from app.business.goal.models.goal_projection import GoalProjection
from app.business.goal.models.parameter_resolution import ParameterResolution


@dataclass(slots=True)
class GoalAnalysis:
    goal: Goal
    parameter_resolution: ParameterResolution
    insights: list[str]
    recommendations: list[str]
    parameters: GoalParameters | None = None 
    projection: GoalProjection | None = None
    status: GoalStatus | None = None