from decimal import Decimal

from app.business.goal.enums.goal_status import GoalStatus
from app.business.goal.models.goal import Goal
from app.business.goal.models.goal_analysis import GoalAnalysis
from app.business.goal.models.goal_parameters import GoalParameters
from app.business.goal.models.goal_projection import GoalProjection
from app.business.goal.models.parameter_resolution import ParameterResolution
from app.business.portfolio.analysis.enums.insight_category import InsightCategory
from app.business.portfolio.analysis.enums.insight_code import InsightCode
from app.business.portfolio.analysis.enums.recommendation_code import RecommendationCode
from app.business.portfolio.analysis.enums.recommendation_priority import RecommendationPriority
from app.business.portfolio.analysis.enums.severity import Severity
from app.business.portfolio.analysis.models.insight import Insight
from app.business.portfolio.analysis.models.recommendation import Recommendation


class GoalAnalyzer:

    AT_RISK_THRESHOLD = Decimal("0.20")

    def analyze(
        self,
        goal: Goal,
        parameters: GoalParameters,
        resolution: ParameterResolution,
        projection: GoalProjection | None,
    ) -> GoalAnalysis:

        status = self._determine_status(
            resolution=resolution,
            projection=projection,
        )

        return GoalAnalysis(
            goal=goal,
            parameters=parameters,
            parameter_resolution=resolution,
            projection=projection,
            status=status,
            insights=self._build_insights(status, projection),
            recommendations=self._build_recommendations(
                status,
                projection,
            ),
        )

    def _determine_status(
        self,
        resolution: ParameterResolution,
        projection: GoalProjection | None,
    ) -> GoalStatus | None:

        if not resolution.complete or projection is None:
            return None

        if projection.funding_gap == Decimal("0"):
            return GoalStatus.ON_TRACK

        ratio = (
            projection.funding_gap
            / projection.projected_goal_amount
        )

        if ratio <= self.AT_RISK_THRESHOLD:
            return GoalStatus.AT_RISK

        return GoalStatus.OFF_TRACK

    def _build_insights(
        self,
        status: GoalStatus | None,
        projection: GoalProjection | None,
    ) -> list[Insight]:

        if status is None or projection is None:
            return []

        insights: list[Insight] = []

        if status == GoalStatus.ON_TRACK:
            insights.append(
                Insight(
                    code=InsightCode.GOAL_ON_TRACK,
                    category=InsightCategory.GOAL,
                    severity=Severity.INFO,
                    title="Goal is on track",
                    description="Your current investment strategy is sufficient to achieve your goal.",
                )
            )

        elif status == GoalStatus.AT_RISK:
            insights.append(
                Insight(
                    code=InsightCode.GOAL_AT_RISK,
                    category=InsightCategory.GOAL,
                    severity=Severity.WARNING,
                    title="Goal needs attention",
                    description="A small increase in your SIP can help you achieve your goal.",
                )
            )

        else:
            insights.append(
                Insight(
                    code=InsightCode.GOAL_OFF_TRACK,
                    category=InsightCategory.GOAL,
                    severity=Severity.HIGH,
                    title="Goal is off track",
                    description="Your current investment strategy is unlikely to achieve your goal.",
                )
            )

        insights.append(
            Insight(
                code=InsightCode.GOAL_FUTURE_AMOUNT,
                category=InsightCategory.GOAL,
                severity=Severity.INFO,
                title="Future goal amount",
                description="Inflation-adjusted target amount.",
                metadata={
                    "future_goal_amount": projection.projected_goal_amount,
                },
            )
        )

        insights.append(
            Insight(
                code=InsightCode.GOAL_PROJECTED_CORPUS,
                category=InsightCategory.GOAL,
                severity=Severity.INFO,
                title="Projected corpus",
                description="Projected value of your investments.",
                metadata={
                    "projected_corpus": projection.projected_corpus,
                },
            )
        )

        if projection.funding_gap > Decimal("0"):
            insights.append(
                Insight(
                    code=InsightCode.GOAL_FUNDING_GAP,
                    category=InsightCategory.GOAL,
                    severity=Severity.WARNING,
                    title="Funding gap",
                    description="Additional investments are required to achieve your goal.",
                    metadata={
                        "funding_gap": projection.funding_gap,
                    },
                )
            )

        return insights

    def _build_recommendations(
        self,
        status: GoalStatus | None,
        projection: GoalProjection | None,
    ) -> list[Recommendation]:

        if status is None or projection is None:
            return []

        if status == GoalStatus.ON_TRACK:
            return [
                Recommendation(
                    code=RecommendationCode.CONTINUE_CURRENT_SIP,
                    priority=RecommendationPriority.LOW,
                    title="Continue current SIP",
                    description="Your current SIP is sufficient.",
                    rationale="Your projected corpus exceeds the required goal amount.",
                )
            ]

        return [
            Recommendation(
                code=RecommendationCode.INCREASE_SIP,
                priority=RecommendationPriority.HIGH,
                title="Increase monthly SIP",
                description="Increase your monthly SIP to achieve your goal.",
                rationale="Your current investment plan leaves a funding gap.",
                metadata={
                    "required_monthly_sip": projection.required_monthly_investment,
                    "additional_monthly_sip": projection.additional_monthly_investment,
                },
            )
        ]