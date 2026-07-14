from dataclasses import dataclass

from app.business.portfolio.analysis.models.diversification_analysis import DiversificationAnalysis
from app.business.portfolio.analysis.models.health_analysis import HealthAnalysis
from app.business.portfolio.analysis.models.insight import Insight
from app.business.portfolio.analysis.models.performance_analysis import PerformanceAnalysis
from app.business.portfolio.analysis.models.recommendation import Recommendation
from app.business.portfolio.analysis.models.risk_analysis import RiskAnalysis
from app.business.portfolio.models import Portfolio
from app.business.portfolio.models.goal_portfolio_snapshot import GoalPortfolioSnapshot


@dataclass(slots=True)
class PortfolioAnalysis:
    portfolio: Portfolio
    performance: PerformanceAnalysis
    diversification: DiversificationAnalysis
    risk: RiskAnalysis
    health: HealthAnalysis
    insights: list[Insight]
    recommendations: list[Recommendation]
    goal_snapshot: GoalPortfolioSnapshot