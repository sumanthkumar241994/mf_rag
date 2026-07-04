from logging import fatal
from app.workflows.advisor.advisor_state import AdvisorState
from app.business.advisor.models.advisor_error import AdvisorError
from app.business.common.models.gateway_result import GatewayResult
from app.business.portfolio.analysis.portfolio_analysis import PortfolioAnalyzer
from app.business.portfolio.gateways.portfolio_gateway import PortfolioGateway
from app.business.portfolio.mapper.portfolio_mapper import PortfolioMapper
from app.business.portfolio.models import Portfolio
from app.infrastructure.api_client.models import GateWayRequestContext


class PortfolioService:
    def __init__(
        self,
        portfolio_gateway: PortfolioGateway,
        portfolio_mapper: PortfolioMapper,
        portfolio_analyzer: PortfolioAnalyzer
    ):
        self._portfolio_gateway = portfolio_gateway
        self._portfolio_mapper = portfolio_mapper
        self._portfolio_analyzer = portfolio_analyzer

    async def analyze(
        self, 
        state: AdvisorState
    ):
        """
        Retrieves and analyzes the customer's portfolio.

        The resulting PortfolioAnalysis is stored in AdvisorState.
        """
        customer_id = state.request.customer_id
        gateway_context = GateWayRequestContext(
            trace_id=state.trace_id,
            conversation_id=state.request.conversation_id,
            customer_id=state.request.customer_id
        )
        result : GatewayResult[Portfolio] = await self._portfolio_gateway.get_portfolio(context=gateway_context)

        if not result.success:
            state.add_error(
                AdvisorError.from_gateway(error=result.error, source='portfolio_gateway')
            )
            return

        portfolio = self._portfolio_mapper.from_falcon_response(result.data)
        portfolio_analysis = self._portfolio_analyzer.analyze(portfolio)

        state.portfolio_analysis = portfolio_analysis