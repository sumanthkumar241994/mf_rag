from app.business.advisor.enums.capabilities import Capability
from app.business.advisor.enums.tool_type import ToolType
from app.business.portfolio.analysis.insight.insight_generator import InsightGenerator
from app.business.portfolio.analysis.portfolio_analysis import PortfolioAnalyzer
from app.business.portfolio.analysis.portfolio_analyzer.diversification_analyzer import DiversificationAnalyzer
from app.business.portfolio.analysis.portfolio_analyzer.health_score_analyzer import HealthAnalyzer
from app.business.portfolio.analysis.portfolio_analyzer.performance_analyzer import PerformanceAnalyzer
from app.business.portfolio.analysis.portfolio_analyzer.risk_analyzer import RiskAnalyzer
from app.business.portfolio.analysis.recommendation.recommendation_engine import RecommendationEngine
from app.business.portfolio.gateways.falcon_portfolio_gateway import FalconPortfolioGateway
from app.business.portfolio.mapper.portfolio_mapper import PortfolioMapper
from app.business.portfolio.service.portfolio_service import PortfolioService
from app.composition.workflow_composition import WorkflowComposition
from app.tools.definitions.tool_definition import ToolDefinition
from app.tools.implementations.portfolio_tool import PortfolioTool
from app.workflows.workflow.service.workflow_service import WorkflowService


class PortfolioComposition:
    def __init__(
        self,
        portfolio_gateway : FalconPortfolioGateway,
        workflow_service: WorkflowService
    ):  
        # Analyzers initialization
        self.performance_analyzer = PerformanceAnalyzer()
        self.diversification_analyzer = DiversificationAnalyzer()
        self.risk_analyzer = RiskAnalyzer()
        self.health_analyzer = HealthAnalyzer()
        self.insight_generator = InsightGenerator()
        self.recommendation_engine = RecommendationEngine()

        # Portfolio Analyzer
        self.portfolio_analyzer = PortfolioAnalyzer(
            performance_analyzer=self.performance_analyzer,
            diversification_analyzer=self.diversification_analyzer,
            risk_analyzer=self.risk_analyzer,
            health_analyzer=self.health_analyzer,
            insight_generator=self.insight_generator,
            recommendation_engine=self.recommendation_engine
        )

        self.portfolio_mapper = PortfolioMapper()

        self.portofio_service = PortfolioService(
            portfolio_gateway=portfolio_gateway,
            portfolio_mapper=self.portfolio_mapper,
            portfolio_analyzer=self.portfolio_analyzer,
            workflow_service=workflow_service
        )

        self.definition = ToolDefinition(
            name=ToolType.PORTFOLIO.value,
            description="Analyze customer's mutual fund portfolio.",
            capability=Capability.PORTFOLIO,
            timeout_seconds=30,
            tags=["portfolio", "analysis", "holdings", "allocation", "returns"]
        )
        
        self.tool = PortfolioTool(
            portfolio_service=self.portofio_service
        )