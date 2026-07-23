from app.business.advisor.enums.capabilities import Capability
from app.business.common.services.base_workflow_service import BaseWorkflowService
from app.business.portfolio.analysis.models.portfolio_analysis import PortfolioAnalysis
from app.observability.tracing import trace_step
from app.workflows.advisor.advisor_state import AdvisorState
from app.business.advisor.models.advisor_error import AdvisorError
from app.business.common.models.gateway_result import GatewayResult
from app.business.portfolio.analysis.portfolio_analysis import PortfolioAnalyzer
from app.business.portfolio.gateways.portfolio_gateway import PortfolioGateway
from app.business.portfolio.mapper.portfolio_mapper import PortfolioMapper
from app.business.portfolio.models import Portfolio
from app.infrastructure.api_client.models import GateWayRequestContext
from app.workflows.workflow.models.workflow_execution import WorkflowExecution
from app.workflows.workflow.service.workflow_service import WorkflowService


class PortfolioService(BaseWorkflowService[PortfolioAnalysis]):
    def __init__(
        self,
        portfolio_gateway: PortfolioGateway,
        portfolio_mapper: PortfolioMapper,
        portfolio_analyzer: PortfolioAnalyzer,
        workflow_service: WorkflowService
    ):
        super().__init__(workflow_service)

        self._portfolio_gateway = portfolio_gateway
        self._portfolio_mapper = portfolio_mapper
        self._portfolio_analyzer = portfolio_analyzer
        self._workflow_service = workflow_service

    @trace_step(
        "portfolio_tool",
        output_mapper=lambda execution: (
        {
            "success": False,
        }
        if execution is None
        else {
            "success": True,
            "interrupted": execution.interrupted,
        }
        ),
        metadata_mapper=lambda result: {
            "tool": "portfolio",
        },
    )
    async def analyze(
        self, 
        state: AdvisorState
    ) -> WorkflowExecution[PortfolioAnalysis]:
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
            state.workflow_execution = None
            state.add_error(
                AdvisorError.from_gateway(error=result.error, source='portfolio_gateway')
            )

            return None

            
        portfolio = self._portfolio_mapper.from_falcon_response(result.data)
        portfolio_analysis = self._portfolio_analyzer.analyze(portfolio)

        execution = self._create_workflow_execution(
            state=state,
            capability=Capability.INVESTMENT,
            result=portfolio_analysis,
            complete=True
        )

        state.workflow_execution = execution
        state.portfolio_analysis = portfolio_analysis

        return execution