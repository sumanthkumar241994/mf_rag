from fastmcp import Client

from app.investment.base.models import GatewayResult, RequestContext
from app.investment.business.customer.models.customer import Customer
from app.investment.business.customer.models.retrieval_customer_request import (
    RetrieveCustomerRequest,
)
from app.investment.business.customer.models.update_nominee_request import UpdateNomineeRequest
from app.investment.business.execution.goal.update_fatca_execution_goal import UpdateFatcaExecutionGoal
from app.investment.business.execution.goal.update_nominee_execution_goal import UpdateNomineeExecutionGoal
from app.investment.workflows.models.workflow_execution import WorkflowExecution
from app.mcp.client.mcp_client import MCPClient


class CustomerClient:

    def __init__(
        self,
        client: MCPClient,
    ):
        self._client = client

    async def retrieve_customer(
        self,
        trace_id: str,
        request: RequestContext,
    ) -> GatewayResult[WorkflowExecution[Customer]]:

        result = await self._client.call(
            tool_name="retrieve_customer",
            response_model=GatewayResult[WorkflowExecution[Customer]],
            request=request,
            trace_id=trace_id,
        )

        # deserialize here
        return GatewayResult.model_validate(result)

    async def update_nominee(
        self,
        trace_id: str,
        request: RequestContext,
        verification_id: str,
        goal: UpdateNomineeExecutionGoal
    ) -> GatewayResult[WorkflowExecution[Customer]]:

        result = await self._client.call(
            tool_name="update_nominee",
            response_model=GatewayResult[WorkflowExecution[Customer]],
            request=request,
            trace_id=trace_id,
            verification_id=verification_id,
            goal=goal,
        )

        # deserialize here
        return GatewayResult.model_validate(result)

    async def update_fatca(
        self,
        trace_id: str,
        request: RequestContext,
        goal: UpdateFatcaExecutionGoal
    ) -> GatewayResult[WorkflowExecution[Customer]]:

        result = await self._client.call(
            tool_name="update_fatca",
            response_model=GatewayResult[WorkflowExecution[Customer]],
            request=request,
            trace_id=trace_id,
            goal=goal,
        )

        # deserialize here
        return GatewayResult.model_validate(result)