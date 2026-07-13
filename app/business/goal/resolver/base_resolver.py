from abc import ABC, abstractmethod

from app.business.customer.models.customer import Customer
from app.business.customer.models.knowledge import CustomerKnowledge
from app.business.goal.models.goal_parameters import GoalParameters
from app.business.goal.models.parameter_resolution import ParameterResolution
from app.business.portfolio.analysis.models.portfolio_analysis import PortfolioAnalysis


class BaseResolver(ABC):

    @abstractmethod
    def resolve(
        self,
        query: str,
        customer: Customer | None,
        porfolio: PortfolioAnalysis | None
    ) -> tuple[GoalParameters, ParameterResolution]:
        """Resolve All parameters required for a goal"""
