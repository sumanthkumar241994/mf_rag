from app.business.customer.models.customer import Customer
from app.business.goal.enums.goal_type import GoalType
from app.business.goal.models.goal_parameters import GoalParameters
from app.business.goal.models.parameter_resolution import ParameterResolution
from app.business.goal.resolver.retirement_resolver import RetirementResolver
from app.business.portfolio.analysis.models.portfolio_analysis import PortfolioAnalysis


class ParameterResolver:
    def __init__(
        self,
        retirement_resolver: RetirementResolver
    ):
        self._resolvers = {
            GoalType.RETIREMENT: retirement_resolver
        }
    
    def resolve(
        self, 
        parameters: GoalParameters, 
        customer: Customer | None,
        portfolio_analysis: PortfolioAnalysis | None
    ) -> tuple[GoalParameters, ParameterResolution]:
        resolver = self._resolvers[parameters.goal_type]

        return resolver.resolve(
            parameters=parameters,
            customer=customer,
            portfolio_analysis=portfolio_analysis
        )

        