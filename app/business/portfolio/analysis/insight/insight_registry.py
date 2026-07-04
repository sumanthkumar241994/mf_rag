from dataclasses import dataclass

from app.business.portfolio.analysis.enums.insight_category import InsightCategory
from app.business.portfolio.analysis.enums.insight_code import InsightCode
from app.business.portfolio.analysis.enums.severity import Severity


@dataclass(slots=True, frozen=True)
class InsightTemplate:
    code: InsightCode
    category: InsightCategory
    severity: Severity
    title: str
    description: str

INSIGHT_REGISTRY: dict[InsightCode, InsightTemplate] = {

    # ---------------------------------------------------------
    # Performance
    # ---------------------------------------------------------

    InsightCode.GOOD_PERFORMANCE: InsightTemplate(
        code=InsightCode.GOOD_PERFORMANCE,
        category=InsightCategory.PERFORMANCE,
        severity=Severity.INFO,
        title="Strong Performance",
        description=(
            "Your portfolio has demonstrated "
            "strong long-term historical performance."
        ),
    ),

    InsightCode.LOW_PERFORMANCE: InsightTemplate(
        code=InsightCode.LOW_PERFORMANCE,
        category=InsightCategory.PERFORMANCE,
        severity=Severity.WARNING,
        title="Performance Needs Review",
        description=(
            "Some investments have delivered "
            "below expected long-term performance."
        ),
    ),

    # ---------------------------------------------------------
    # Diversification
    # ---------------------------------------------------------

    InsightCode.GOOD_DIVERSIFICATION: InsightTemplate(
        code=InsightCode.GOOD_DIVERSIFICATION,
        category=InsightCategory.DIVERSIFICATION,
        severity=Severity.INFO,
        title="Well Diversified",
        description=(
            "Your investments are well diversified "
            "across schemes and fund houses."
        ),
    ),

    InsightCode.LOW_DIVERSIFICATION: InsightTemplate(
        code=InsightCode.LOW_DIVERSIFICATION,
        category=InsightCategory.DIVERSIFICATION,
        severity=Severity.WARNING,
        title="Portfolio Concentration",
        description=(
            "Your portfolio is concentrated across "
            "relatively few investments."
        ),
    ),

    # ---------------------------------------------------------
    # Risk
    # ---------------------------------------------------------

    InsightCode.HIGH_PORTFOLIO_RISK: InsightTemplate(
        code=InsightCode.HIGH_PORTFOLIO_RISK,
        category=InsightCategory.RISK,
        severity=Severity.CRITICAL,
        title="High Portfolio Risk",
        description=(
            "Your portfolio currently carries "
            "a high overall investment risk."
        ),
    ),

    InsightCode.HIGH_RISK_CONTRIBUTOR: InsightTemplate(
        code=InsightCode.HIGH_RISK_CONTRIBUTOR,
        category=InsightCategory.RISK,
        severity=Severity.INFO,
        title="Largest Risk Contributor",
        description=(
            "{scheme_name} contributes the highest "
            "proportion of risk in your portfolio."
        ),
    ),

    # ---------------------------------------------------------
    # Health
    # ---------------------------------------------------------

    InsightCode.GOOD_HEALTH: InsightTemplate(
        code=InsightCode.GOOD_HEALTH,
        category=InsightCategory.HEALTH,
        severity=Severity.INFO,
        title="Healthy Portfolio",
        description=(
            "Overall your portfolio appears "
            "to be in good health."
        ),
    ),

    InsightCode.LOW_HEALTH: InsightTemplate(
        code=InsightCode.LOW_HEALTH,
        category=InsightCategory.HEALTH,
        severity=Severity.WARNING,
        title="Portfolio Needs Attention",
        description=(
            "Overall portfolio health can "
            "be improved."
        ),
    ),
}