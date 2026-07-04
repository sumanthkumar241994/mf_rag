

from typing import Any
from app.business.portfolio.analysis.enums.insight_code import InsightCode
from app.business.portfolio.analysis.insight.insight_registry import INSIGHT_REGISTRY
from app.business.portfolio.analysis.models.insight import Insight
from app.business.portfolio.analysis.models.diversification_analysis import DiversificationAnalysis
from app.business.portfolio.analysis.models.health_analysis import HealthAnalysis
from app.business.portfolio.analysis.models.performance_analysis import PerformanceAnalysis
from app.business.portfolio.analysis.models.risk_analysis import RiskAnalysis
from app.business.portfolio.enums import PerformanceRating


class InsightGenerator:
    
    def generate(
        self,
        performance: PerformanceAnalysis,
        diversification: DiversificationAnalysis,
        risk: RiskAnalysis,
        health: HealthAnalysis
    ) -> list[Insight]:

        insights: list[Insight] = []
        insights.extend(self._performance_insights(performance))
        insights.extend(self._diversification_insights(diversification))
        insights.extend(self._risk_insights(risk))
        insights.extend(self._health_insights(health))

        return insights

    
    def _performance_insights(self, performance: PerformanceAnalysis) -> list[Insight]:
        insights: list[Insight] = []

        if performance.performance_rating == PerformanceRating.EXCELLENT.value:
            insights.append(
                self._build_insight(InsightCode.GOOD_PERFORMANCE)
            )
        elif performance.performance_rating == PerformanceRating.NEEDS_REVIEW.value:
            insights.append(
                self._build_insight(InsightCode.LOW_PERFORMANCE)
            )
        return insights
    
    def _diversification_insights(self, diversification: DiversificationAnalysis) -> list[Insight]:
        insights: list[Insight] = []

        if diversification.is_well_diversified:
            insights.append(
                self._build_insight(InsightCode.GOOD_DIVERSIFICATION)
            )
        else:
            insights.append(
                self._build_insight(InsightCode.LOW_DIVERSIFICATION)
            )
        
        return insights

    def _risk_insights(self, risk: RiskAnalysis) -> list[Insight]:
        insights : list[Insight] = []

        if risk.portfolio_risk_rating in ("HIGH", "VERY_HIGH"):
            insights.append(
                self._build_insight(InsightCode.HIGH_PORTFOLIO_RISK)
            )
        contributor = risk.highest_risk_contributor

        if contributor:
            insights.append(
                self._build_insight(
                    InsightCode.HIGH_RISK_CONTRIBUTOR, 
                    scheme_name=contributor.scheme_name,
                    metadata={
                        "scheme_code": contributor.scheme_code,
                        "scheme_name": contributor.scheme_name,
                        "allocation": contributor.allocation_percentage,
                        "portfolio_risk_contribution": contributor.portfolio_risk_contribution
                    }
                )
            )
        
        return insights
    
    def _health_insights(self, health: HealthAnalysis) -> list[Insight]:
        insights : list[Insight] = []

        if health.health_rating in ("EXCELLENT", "GOOD"):
            insights.append(
                self._build_insight(InsightCode.GOOD_HEALTH)
            )
        elif health.health_rating in ("POOR", "NEEDS_IMPROVEMENT"):
            insights.append(
                self._build_insight(InsightCode.LOW_HEALTH)
            )
        
        return insights

    @staticmethod
    def _build_insight(code: InsightCode, *, metadata: dict[str, Any] | None = None ,**kwargs) -> Insight:
        template = INSIGHT_REGISTRY[code]

        return Insight(
            code=template.code,
            category=template.category,
            severity=template.severity,
            title=template.title,
            description=template.description.format(**kwargs),
            metadata=metadata
        )