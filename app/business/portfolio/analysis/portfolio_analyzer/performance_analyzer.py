from decimal import Decimal, ROUND_HALF_UP

from app.business.portfolio.models.holding import Holding
from app.business.portfolio.models.portfolio import Portfolio
from app.business.portfolio.analysis.models.performance_analysis import PerformanceAnalysis, PerformanceHolding

from app.business.portfolio.enums import PerformanceRating

class PerformanceAnalyzer:
    FIVE_YEAR_WEIGHT = Decimal('0.50')
    THREE_YEAR_WEIGHT = Decimal('0.30')
    ONE_YEAR_WEIGHT = Decimal('0.20')

    def analyze(self, portfolio: Portfolio) -> PerformanceAnalysis:
        holdings = portfolio.holdings

        if not holdings:
            return PerformanceAnalysis(
                score=Decimal("0"),
                performance_rating=PerformanceRating.UNKNOWN.value,
                average_five_year_return=Decimal('0'),
                average_three_year_return=Decimal('0'),
                average_one_year_return=Decimal('0')
            )

        scored_holdings: list[tuple[Holding, Decimal]]= []

        for holding in holdings:
            score = self._calculate_performance_score(holding)
            scored_holdings.append((holding,score))

        scores = [score for _, score in scored_holdings]
        average_score = (sum(scores)/ Decimal(len(scores))).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)

        best = max(scored_holdings, key=lambda x: x[1])

        weakest = None

        if len(scored_holdings) > 1:
            weakest = min(scored_holdings, key=lambda x: x[1])

            if weakest[1] == best[1]:
                weakest = None

        return PerformanceAnalysis(
            average_one_year_return= self._average(holdings, "one_year_return"),
            average_three_year_return=self._average(holdings, "three_year_return"),
            average_five_year_return=self._average(holdings, "five_year_return"),
            score=average_score,
            performance_rating=self._performance_rating(average_score),
            best_performing_holding=self._to_summary(best[0],best[1]),
            worst_performing_holding=self._to_summary(weakest[0], weakest[1]) if weakest else None
        )


    def _calculate_performance_score(self, holding: Holding) -> Decimal:
        weighted_sum = Decimal('0')
        total_weight = Decimal('0')

        returns = [
                (holding.scheme.five_year_return, self.FIVE_YEAR_WEIGHT),
                (holding.scheme.three_year_return, self.THREE_YEAR_WEIGHT),
                (holding.scheme.one_year_return, self.ONE_YEAR_WEIGHT)
        ]

        for value, weight in returns:
            if value is None:
                continue

            weighted_sum +=value * weight
            total_weight += weight
        
        if total_weight == 0:
            return Decimal('0')
        
        return (weighted_sum/total_weight).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)


    @staticmethod
    def _average(holdings: list[Holding], attribute: str) -> Decimal:
        if not holdings:
            return Decimal('0')
        
        total = sum(getattr(h.scheme, attribute) for h in holdings)
        return (total / Decimal(len(holdings))).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)

    @staticmethod
    def _performance_rating(score: Decimal) -> str:
        if score > Decimal('20'):
            return PerformanceRating.EXCELLENT.value
        if score > Decimal('15'):
            return PerformanceRating.GOOD.value
        if score > Decimal('10'):
            return PerformanceRating.AVERAGE.value
        
        return PerformanceRating.NEEDS_REVIEW.value


    @staticmethod
    def _to_summary(holding: Holding, score: Decimal) -> PerformanceHolding:
        return PerformanceHolding(
            scheme_code=holding.scheme.scheme_code,
            scheme_name=holding.scheme.name,
            category=holding.scheme.category,
            amc_name=holding.scheme.amc_name,
            one_year_return=holding.scheme.one_year_return,
            three_year_return=holding.scheme.three_year_return,
            five_year_return=holding.scheme.five_year_return,
            performance_score=score
        )
