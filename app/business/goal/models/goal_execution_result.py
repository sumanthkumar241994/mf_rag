from dataclasses import dataclass

from app.business.goal.models.goal_analysis import GoalAnalysis


@dataclass(slots=True)
class GoalExecutionResult:
    analysis: GoalAnalysis
    requires_follow_up: bool
    follow_up_questions: list[str]