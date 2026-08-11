# app/mcp/tools/customer.py

from app.business.customer.models.customer import Customer
from app.investment.base.models import GatewayResult, RequestContext
from app.investment.business.customer.customer_service import CustomerService
from app.investment.business.customer.models.retrieval_customer_request import RetrieveCustomerRequest
from app.investment.business.customer.models.update_fatca_request import UpdateFatcaRequest
from app.investment.business.customer.models.update_nominee_request import UpdateNomineeRequest
from app.investment.business.execution.goal.update_fatca_execution_goal import UpdateFatcaExecutionGoal
from app.investment.business.execution.goal.update_nominee_execution_goal import UpdateNomineeExecutionGoal
from app.investment.workflows.investment_state import InvestmentState
from app.workflows.workflow.models.workflow_execution import WorkflowExecution
from fastmcp import FastMCP


def register_customer_tools(mcp: FastMCP, customer_service: CustomerService) -> None:
    """
    Registers customer-related MCP tools.
    """

    @mcp.tool(name="retrieve_customer", description="Retrieve customer profile, KYC, bank and nominee details.")
    async def retrieve_customer(trace_id: str, request: RequestContext) -> GatewayResult[WorkflowExecution[Customer]]:
        request = RetrieveCustomerRequest(
            trace_id=trace_id,
            request=request,
        )
        return await customer_service.retrieve(request)
    
    @mcp.tool(name="update_nominee", description="update nominee details.")
    async def update_nominee(trace_id: str, request: RequestContext, goal: UpdateNomineeExecutionGoal) -> GatewayResult[WorkflowExecution[Customer]]:
        request = UpdateNomineeRequest(
            trace_id=trace_id,
            request=request,
            goal=goal
        )
        return await customer_service.update_nominee(request)

    @mcp.tool(name="update_nominee", description="update nominee details.")
    async def update_fatca(trace_id: str, request: RequestContext, goal: UpdateFatcaExecutionGoal) -> GatewayResult[WorkflowExecution[Customer]]:
        request = UpdateFatcaRequest(
            trace_id=trace_id,
            request=request,
            goal=goal
        )
        return await customer_service.update_fatca(request)