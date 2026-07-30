from dataclasses import asdict
from app.business.customer.models.customer import Customer
from app.investment.base.models import GatewayResult, RequestContext, WorkflowError
from app.investment.business.customer.models.retrieval_customer_request import (
    RetrieveCustomerRequest,
)
from app.investment.workflows.investment_state import InvestmentState
from app.mcp.client.customer_client import CustomerClient
from app.workflows.workflow.models.workflow_execution import WorkflowExecution


class CustomerNode:
    """
    LangGraph node responsible for retrieving customer information
    required for the investment workflow.
    """

    def __init__(
        self,
        customer_client: CustomerClient,
    ) -> None:
        self._customer_client = customer_client

    async def __call__(
        self,
        state: InvestmentState,
    ) -> InvestmentState:
        """
        Retrieve customer details through MCP and update workflow state.
        """

        request = RetrieveCustomerRequest(
            trace_id=state.trace_id,
            request=RequestContext(**asdict(state.request)),
        )

        result: GatewayResult[
            WorkflowExecution[Customer]
        ] = await self._customer_client.retrieve_customer(
            request=request,
        )

        if not result.success:
            state.workflow_execution = None
            state.add_error(
                WorkflowError.from_gateway(
                    error=result.error,
                    source="customer_mcp",
                )
            )
            return state

        execution = result.data

        state.workflow_execution = execution
        state.customer = execution.result

        return state