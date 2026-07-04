from abc import ABC, abstractmethod

from app.workflows.advisor.advisor_state import AdvisorState
from app.business.advisor.models.planner_result import PlannerResult


class Planner(ABC):
    @abstractmethod
    async def plan(self, state: AdvisorState) -> PlannerResult:
        raise NotImplementedError