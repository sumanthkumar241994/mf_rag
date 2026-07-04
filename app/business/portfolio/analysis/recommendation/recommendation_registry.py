from app.business.portfolio.analysis.enums.recommendation_code import RecommendationCode
from app.business.portfolio.analysis.enums.recommendation_priority import RecommendationPriority
from app.business.portfolio.analysis.models.recommendation import Recommendation


RECOMMENDATION_REGISTRY: dict[RecommendationCode,Recommendation] = {

    RecommendationCode.DIVERSIFY_PORTFOLIO: Recommendation(
        code=RecommendationCode.DIVERSIFY_PORTFOLIO,
        priority=RecommendationPriority.HIGH,
        title="Improve Diversification",
        description=(
            "Consider investing across additional schemes or "
            "fund houses to reduce concentration risk."
        ),
        rationale=(
            "A diversified portfolio generally reduces "
            "investment concentration risk."
        ),
    ),

    RecommendationCode.REDUCE_PORTFOLIO_RISK: Recommendation(
        code=RecommendationCode.REDUCE_PORTFOLIO_RISK,
        priority=RecommendationPriority.CRITICAL,
        title="Reduce Portfolio Risk",
        description=(
            "Consider increasing allocation towards lower-risk "
            "funds if it aligns with your financial goals."
        ),
        rationale=(
            "Reducing portfolio risk may help improve "
            "long-term stability."
        ),
    ),

    RecommendationCode.REDUCE_CONCENTRATION: Recommendation(
        code=RecommendationCode.REDUCE_CONCENTRATION,
        priority=RecommendationPriority.HIGH,
        title="Reduce Concentration",
        description=(
            "Review your allocation to {scheme_name} as it "
            "contributes the largest share of portfolio risk."
        ),
        rationale=(
            "Reducing concentration can improve diversification."
        ),
    ),

    RecommendationCode.REVIEW_UNDERPERFORMING_FUNDS: Recommendation(
        code=RecommendationCode.REVIEW_UNDERPERFORMING_FUNDS,
        priority=RecommendationPriority.MEDIUM,
        title="Review Underperforming Funds",
        description=(
            "Review funds that have consistently "
            "underperformed over longer investment horizons."
        ),
        rationale=(
            "Periodic portfolio reviews help maintain "
            "investment quality."
        ),
    ),

    RecommendationCode.MAINTAIN_PORTFOLIO: Recommendation(
        code=RecommendationCode.MAINTAIN_PORTFOLIO,
        priority=RecommendationPriority.LOW,
        title="Maintain Current Portfolio",
        description=(
            "Your portfolio appears healthy. Continue "
            "investing according to your financial plan."
        ),
        rationale=(
            "No major issues requiring immediate action "
            "were identified."
        ),
    ),
}