from dataclasses import dataclass, field

from app.business.goal.models.goal_parameters import GoalParameters


@dataclass(slots=True)
class ParameterResolution:
    missing_parameters: list[str]
    follow_up_questions: list[str]

    @property
    def complete(self):
        return len(self.missing_parameters) == 0