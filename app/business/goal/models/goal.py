from dataclasses import dataclass

from app.business.goal.enums.goal_type import GoalType


@dataclass(slots=True)
class Goal:
    goal_type: GoalType
    title: str
    description: str | None = None