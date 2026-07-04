from decimal import Decimal, ROUND_HALF_UP

from app.business.portfolio.analysis.models.risk_analysis import (
    RiskAnalysis,
    RiskContributor,
)
from app.business.portfolio.models.portfolio import Portfolio


class RiskAnalyzer:

    def analyze(self, portfolio: Portfolio) -> RiskAnalysis:

        holdings = portfolio.holdings

        if not holdings:
            return RiskAnalysis(
                portfolio_risk_score=Decimal("0"),
                portfolio_risk_rating="UNKNOWN",
                highest_risk_contributor=None,
                weighted_risk_score=Decimal("0"),
                equity_allocation=Decimal("0"),
                debt_allocation=Decimal("0"),
                hybrid_allocation=Decimal("0"),
                solution_allocation=Decimal("0"),
                others_allocation=Decimal("0"),
            )

        weighted_score = self._weighted_portfolio_risk(
            portfolio,
        )

        highest = self._highest_risk_contributor(portfolio)

        return RiskAnalysis(
            score=self._risk_score(weighted_score),
            portfolio_risk_rating=self._risk_rating(weighted_score),
            highest_risk_contributor=highest,
            weighted_risk_score=weighted_score,
            equity_allocation=portfolio.category_allocation.equity.allocation_percentage,
            debt_allocation=portfolio.category_allocation.debt.allocation_percentage,
            hybrid_allocation=portfolio.category_allocation.hybrid.allocation_percentage,
            solution_allocation=portfolio.category_allocation.solution.allocation_percentage,
            others_allocation=portfolio.category_allocation.others.allocation_percentage,
        )

    # ---------------------------------------------------------

    def _weighted_portfolio_risk(self, portfolio: Portfolio) -> Decimal:

        total = Decimal("0")
        total_value = portfolio.totals.current_value

        if total_value == 0:
            return Decimal("0")

        for holding in portfolio.holdings:
            allocation = holding.current_value/ total_value

            risk = Decimal(holding.scheme.riskometer)

            total += allocation * risk

        return total.quantize(
            Decimal("0.01"),
            rounding=ROUND_HALF_UP,
        )

    # ---------------------------------------------------------


    def _highest_risk_contributor(self, portfolio: Portfolio) -> RiskContributor | None:

        if not portfolio.holdings:
            return None

        total_value = portfolio.totals.current_value

        highest = None
        highest_score = Decimal("0")

        for holding in portfolio.holdings:

            if total_value == 0:
                allocation = Decimal("0")
            else:
                allocation = holding.current_value* Decimal("100")/ total_value

            contribution = allocation * Decimal(holding.scheme.riskometer)

            if contribution > highest_score:
                highest_score = contribution
                highest = (holding, allocation, contribution)

        if highest is None:
            return None

        holding, allocation, contribution = highest

        return RiskContributor(
            scheme_code=holding.scheme.scheme_code,
            scheme_name=holding.scheme.name,
            category=holding.scheme.category,
            allocation_percentage=allocation.quantize(Decimal("0.01")),
            riskometer=holding.scheme.riskometer,
            riskometer_display=holding.scheme.riskometer_display,
            portfolio_risk_contribution=contribution.quantize(Decimal('0.01'))
        )

    # ---------------------------------------------------------

    @staticmethod
    def _risk_score(weighted: Decimal) -> Decimal:
        score = (weighted/ Decimal("6")) * Decimal("100")

        return score.quantize(Decimal("0.01"),rounding=ROUND_HALF_UP)

    # ---------------------------------------------------------

    @staticmethod
    def _risk_rating(weighted: Decimal) -> str:
        if weighted < Decimal("1.5"):
            return "VERY_LOW"
        if weighted < Decimal("2.5"):
            return "LOW"
        if weighted < Decimal("3.5"):
            return "MODERATE"
        if weighted < Decimal("4.5"):
            return "HIGH"

        return "VERY_HIGH"