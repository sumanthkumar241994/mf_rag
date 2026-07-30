from fastmcp import Client

from app.investment.base.models import GatewayResult
from app.investment.business.customer.models.customer import Customer
from app.investment.business.customer.models.retrieval_customer_request import (
    RetrieveCustomerRequest,
)
from app.mcp.client.mcp_client import MCPClient
from app.workflows.workflow.models.workflow_execution import WorkflowExecution


class CustomerClient:

    def __init__(
        self,
        client: MCPClient,
    ):
        self._client = client

    async def retrieve_customer(
        self,
        request: RetrieveCustomerRequest,
    ) -> GatewayResult[WorkflowExecution[Customer]]:

        result = await self._client.call(
            tool_name="retrieve_customer",
            request=request,
            response_model=GatewayResult[WorkflowExecution[Customer]]
        )

        # deserialize here
        return GatewayResult.model_validate(result)