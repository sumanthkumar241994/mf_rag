from decimal import Decimal

from app.business.portfolio.analysis.models.diversification_analysis import DiversificationAnalysis
from app.business.portfolio.models.portfolio import Portfolio


class DiversificationAnalyzer:

    def analyze(self, portfolio: Portfolio) -> DiversificationAnalysis:
        totals = portfolio.totals
        summary = portfolio.summary

        scheme_score = self._scheme_score(totals.scheme_count)
        amc_score = self._amc_score(totals.amc_count)
        concentration_score = self._holding_concentration_score(summary.largest_holding.allocation_percentage if summary.largest_holding else Decimal('0'))
        amc_concentration_score = self._amc_concentration_score(summary.highest_exposure_amc_percentage)

        score = scheme_score + amc_score + concentration_score + amc_concentration_score

        return DiversificationAnalysis(
            score=score,
            diversification_rating=self._rating(score),
            scheme_count=totals.scheme_count,
            holding_count=totals.holding_count,
            folio_count=totals.folio_count,
            amc_count=totals.amc_count,
            highest_amc_percentage=amc_concentration_score,
            largest_holding_percentage=summary.largest_holding.allocation_percentage if summary.largest_holding else Decimal('0'),
            is_well_diversified= score>=75
        )


    @staticmethod
    def _scheme_score(scheme_count: int) -> int:
        if scheme_count <=1:
            return 10
        elif scheme_count <=4:
            return 25
        elif scheme_count <=8:
            return 40
        
        return 35

    @staticmethod
    def _amc_score(amc_count: int) -> int:
        if amc_count <=1:
            return 5
        elif amc_count ==2:
            return 15
        elif amc_count <=5:
            return 25
        
        return 20
    
    @staticmethod
    def _holding_concentration_score(largest_holding: Decimal) -> int:
        if largest_holding < Decimal("20"):
            return 20
        if largest_holding < Decimal("35"):
            return 15
        if largest_holding < Decimal("50"):
            return 8

        return 2

    @staticmethod
    def _amc_concentration_score(highest_amc: Decimal) -> int:
        if highest_amc < Decimal("25"):
            return 15
        if highest_amc < Decimal("40"):
            return 10
        if highest_amc < Decimal("60"):
            return 5

        return 0

    @staticmethod
    def _rating(score: int) -> str:
        if score >= 90:
            return "EXCELLENT"
        if score >= 75:
            return "GOOD"
        if score >= 60:
            return "AVERAGE"

        return "POOR"