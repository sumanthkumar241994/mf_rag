from abc import ABC, abstractmethod

from app.business.goal.models.goal_parameters import GoalParameters
from app.business.goal.models.goal_projection import GoalProjection


class BaseCalculator(ABC):
    @abstractmethod
    def calculate(self, parameters: GoalParameters) -> GoalProjection:
        """Goal calculator"""