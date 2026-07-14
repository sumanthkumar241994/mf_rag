

from app.business.portfolio.analysis.insight.insight_generator import InsightGenerator
from app.business.portfolio.analysis.models.portfolio_analysis import PortfolioAnalysis
from app.business.portfolio.analysis.portfolio_analyzer.diversification_analyzer import DiversificationAnalyzer
from app.business.portfolio.analysis.portfolio_analyzer.health_score_analyzer import HealthAnalyzer
from app.business.portfolio.analysis.portfolio_analyzer.performance_analyzer import PerformanceAnalyzer
from app.business.portfolio.analysis.portfolio_analyzer.risk_analyzer import RiskAnalyzer
from app.business.portfolio.analysis.recommendation.recommendation_engine import RecommendationEngine
from app.business.portfolio.models import Portfolio
from app.business.portfolio.models.goal_portfolio_snapshot import GoalPortfolioSnapshot


class PortfolioAnalyzer:

    def __init__(
        self,
        performance_analyzer: PerformanceAnalyzer,
        diversification_analyzer: DiversificationAnalyzer,
        risk_analyzer: RiskAnalyzer,
        health_analyzer: HealthAnalyzer,
        insight_generator: InsightGenerator,
        recommendation_engine: RecommendationEngine
    ):
        self._performance_analyzer = performance_analyzer
        self._diversification_analyzer = diversification_analyzer
        self._risk_analyzer = risk_analyzer
        self._health_analyzer = health_analyzer
        self._insight_generator = insight_generator
        self._recommendation_engine = recommendation_engine
    
    def analyze(self, portfolio: Portfolio) -> PortfolioAnalysis:
        performance = self._performance_analyzer.analyze(portfolio)
        diversification = self._diversification_analyzer.analyze(portfolio)
        risk = self._risk_analyzer.analyze(portfolio)
        health = self._health_analyzer.analyze(performace=performance, diversification=diversification, risk=risk)

        insights = self._insight_generator.generate(
            performance,
            diversification,
            risk,
            health
        )

        recommendations = self._recommendation_engine.generate(insights)

        goal_portfolio_snapshot = GoalPortfolioSnapshot(
            current_corpus=portfolio.totals.current_value,
            total_investment=portfolio.totals.net_investment,
            monthly_investment=portfolio.summary.monthly_sip,
            equity_value=portfolio.category_allocation.equity.current_value,
            debt_value=portfolio.category_allocation.debt.current_value,
            hybrid_value=portfolio.category_allocation.hybrid.current_value,
        )

        return PortfolioAnalysis(
            portfolio=portfolio,
            performance=performance,
            diversification=diversification,
            risk=risk,
            health=health,
            insights=insights,
            recommendations=recommendations,
            goal_snapshot=goal_portfolio_snapshot
        )
