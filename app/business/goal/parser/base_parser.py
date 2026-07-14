from abc import ABC, abstractmethod

from app.business.goal.models.goal_parameters import GoalParameters


class BaseParser(ABC):
    @abstractmethod
    def can_parse(self, query: str) -> bool:
        """Returns True if this parser can parse the query"""

    @abstractmethod
    def parse(self, query: str) -> GoalParameters:
        """Extract goal parameters from query"""
    