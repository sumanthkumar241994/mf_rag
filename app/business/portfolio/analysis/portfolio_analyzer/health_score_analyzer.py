from decimal import ROUND_HALF_UP, Decimal

from app.business.portfolio.analysis.models.diversification_analysis import DiversificationAnalysis
from app.business.portfolio.analysis.models.health_analysis import HealthAnalysis
from app.business.portfolio.analysis.models.performance_analysis import PerformanceAnalysis
from app.business.portfolio.analysis.models.risk_analysis import RiskAnalysis


class HealthAnalyzer:
    PERFORMANCE_WEIGHT = Decimal("0.40")
    DIVERSIFICATION_WEIGHT = Decimal("0.35")
    RISK_WEIGHT = Decimal("0.25")

    def analyze(
        self, 
        performace: PerformanceAnalysis,
        diversification: DiversificationAnalysis,
        risk: RiskAnalysis
    ) -> HealthAnalysis:
        score = self._calculate_score(performace, diversification, risk)
        
        return HealthAnalysis(
            health_score=score,
            health_rating=self._rating(score)
        )

    
    def _calculate_score(
        self,
        performace: PerformanceAnalysis,
        diversification: DiversificationAnalysis,
        risk: RiskAnalysis
    ):
        performance_score = performace.score * self.PERFORMANCE_WEIGHT
        diversification_score = diversification.score * self.DIVERSIFICATION_WEIGHT
        risk_score = (Decimal('100') - risk.score) * self.RISK_WEIGHT

        score = performance_score + diversification_score + risk_score
        return int(score.quantize(Decimal("1"), rounding=ROUND_HALF_UP))

    
    @staticmethod
    def _rating(score: int) -> str:
        if score >= 90:
            return "EXCELLENT"
        if score >= 75:
            return "GOOD"
        if score >= 60:
            return "AVERAGE"
        if score >= 40:
            return "NEEDS_IMPROVEMENT"

        return "POOR"

    
