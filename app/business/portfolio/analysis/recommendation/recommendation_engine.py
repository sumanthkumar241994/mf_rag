from copy import deepcopy

from app.business.portfolio.analysis.enums.insight_code import InsightCode
from app.business.portfolio.analysis.models.insight import Insight
from app.business.portfolio.analysis.enums.recommendation_code import RecommendationCode
from app.business.portfolio.analysis.models.recommendation import Recommendation
from app.business.portfolio.analysis.recommendation.recommendation_registry import RECOMMENDATION_REGISTRY


class RecommendationEngine:

    def generate(self, insights: list[Insight]) -> list[Recommendation]:

        recommendations: list[Recommendation] = []
        recommendation_codes: set[RecommendationCode] = set()

        for insight in insights:
            recommendation = self._recommend(insight)

            if recommendation is None:
                continue

            # Avoid duplicate recommendations
            if recommendation.code in recommendation_codes:
                continue

            recommendation_codes.add(recommendation.code)
            recommendations.append(recommendation)

        # Healthy portfolio with no recommendations
        if not recommendations:
            recommendations.append(self._build(RecommendationCode.MAINTAIN_PORTFOLIO))

        return recommendations


    def _recommend(self,insight: Insight) -> Recommendation | None:

        match insight.code:

            case InsightCode.LOW_DIVERSIFICATION:
                return self._recommend_diversification(insight)

            case InsightCode.LOW_PERFORMANCE:
                return self._recommend_performance(insight)

            case InsightCode.HIGH_PORTFOLIO_RISK:
                return self._recommend_risk(insight)

            case InsightCode.HIGH_RISK_CONTRIBUTOR:
                return self._recommend_concentration(insight)

            case InsightCode.GOOD_HEALTH:
                return self._recommend_healthy_portfolio(insight)

            case _:
                return None


    def _recommend_diversification(self, insight: Insight) -> Recommendation:
        return self._build(RecommendationCode.DIVERSIFY_PORTFOLIO)


    def _recommend_performance(self, insight: Insight) -> Recommendation:
        return self._build(RecommendationCode.REVIEW_UNDERPERFORMING_FUNDS)


    def _recommend_risk(self, insight: Insight) -> Recommendation:
        return self._build(RecommendationCode.REDUCE_PORTFOLIO_RISK)


    def _recommend_concentration(self,insight: Insight) -> Recommendation:

        return self._build(
            RecommendationCode.REDUCE_CONCENTRATION,
            scheme_name=insight.metadata.get("scheme_name", ""),
            metadata=insight.metadata,
        )


    def _recommend_healthy_portfolio(self, insight: Insight) -> Recommendation:

        return self._build(RecommendationCode.MAINTAIN_PORTFOLIO)


    @staticmethod
    def _build(code: RecommendationCode, *, metadata: dict | None = None, **kwargs,) -> Recommendation:

        template = deepcopy(RECOMMENDATION_REGISTRY[code])
        template.description = template.description.format(**kwargs)
        template.rationale = template.rationale.format(**kwargs)
        template.metadata.update(metadata or {})

        return template