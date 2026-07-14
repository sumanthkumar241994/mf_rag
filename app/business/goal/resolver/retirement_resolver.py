from decimal import Decimal

from app.business.customer.models.customer import Customer
from app.business.goal.enums.goal_parameter import GoalParameter
from app.business.goal.models.goal_parameters import GoalParameters
from app.business.goal.models.parameter_resolution import ParameterResolution
from app.business.goal.resolver.base_resolver import BaseResolver
from app.business.portfolio.analysis.models.portfolio_analysis import PortfolioAnalysis


class RetirementResolver(BaseResolver):

    def __init__(
        self,
        expected_return: Decimal = Decimal("12"),
        inflation_rate: Decimal = Decimal("6"),
    ):
        self._expected_return = expected_return
        self._inflation_rate = inflation_rate

    def resolve(
        self,
        parameters: GoalParameters,
        customer: Customer | None,
        portfolio_analysis: PortfolioAnalysis | None,
    ) -> tuple[GoalParameters, ParameterResolution]:

        self._enrich_customer(parameters, customer)
        self._enrich_portfolio(parameters, portfolio_analysis)
        self._apply_defaults(parameters)
        self._derive_parameters(parameters)

        resolution = self._validate(parameters)

        return parameters, resolution

    def _enrich_customer(self, parameters: GoalParameters, customer: Customer | None) -> None:

        if customer is None:
            return

        if parameters.current_age is None and customer.profile.date_of_birth is not None:
            parameters.current_age = customer.profile.age

    def _enrich_portfolio(self, parameters: GoalParameters, portfolio_analysis: PortfolioAnalysis | None) -> None:

        if portfolio_analysis is None:
            return

        snapshot = portfolio_analysis.goal_snapshot

        if parameters.current_corpus is None:
            parameters.current_corpus = snapshot.current_corpus

        if parameters.monthly_investment is None:
            parameters.monthly_investment = snapshot.monthly_investment


    def _apply_defaults(self, parameters: GoalParameters) -> None:
        if parameters.expected_return is None:
            parameters.expected_return = self._expected_return

        if parameters.inflation_rate is None:
            parameters.inflation_rate = self._inflation_rate

    def _derive_parameters(self, parameters: GoalParameters) -> None:

        if parameters.target_years is None and parameters.current_age is not None and parameters.retirement_age is not None:
            years = parameters.retirement_age - parameters.current_age

            if years > 0:
                parameters.target_years = years

    def _validate(
        self,
        parameters: GoalParameters,
    ) -> ParameterResolution:

        missing_parameters: list[GoalParameter] = []
        follow_up_questions: list[str] = []

        if parameters.goal_amount is None:
            missing_parameters.append(
                GoalParameter.GOAL_AMOUNT,
            )
            follow_up_questions.append(
                "What retirement corpus would you like to accumulate?"
            )

        if parameters.target_years is None and parameters.retirement_age is None:
            missing_parameters.append(
                GoalParameter.RETIREMENT_AGE,
            )

            follow_up_questions.append(
                "At what age would you like to retire?"
            )

        if parameters.current_corpus is None:
            missing_parameters.append(
                GoalParameter.CURRENT_CORPUS,
            )

        if parameters.monthly_investment is None:
            missing_parameters.append(
                GoalParameter.MONTHLY_INVESTMENT,
            )

        if parameters.expected_return is None:
            missing_parameters.append(
                GoalParameter.EXPECTED_RETURN,
            )

        if parameters.inflation_rate is None:
            missing_parameters.append(
                GoalParameter.INFLATION_RATE,
            )

        return ParameterResolution(
            missing_parameters=missing_parameters,
            follow_up_questions=follow_up_questions,
        )