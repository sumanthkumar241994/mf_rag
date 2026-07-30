# app/mcp/tools/customer.py

from app.business.customer.models.customer import Customer
from app.investment.base.models import GatewayResult, RequestContext
from app.investment.business.customer.customer_service import CustomerService
from app.investment.business.customer.models.retrieval_customer_request import RetrieveCustomerRequest
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