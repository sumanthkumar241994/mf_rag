from dataclasses import asdict
from typing import cast

from app.investment.base.models import GatewayResult, RequestContext
from app.investment.business.execution.customer.handlers.customer_update_action_handler import (
    CustomerUpdateActionHandler,
)
from app.investment.business.execution.goal.update_fatca_execution_goal import (
    UpdateFatcaExecutionGoal,
)
from app.investment.workflows.investment_state import (
    InvestmentState,
)
from app.mcp.client.customer_client import CustomerClient


class FatcaUpdateActionHandler(CustomerUpdateActionHandler):

    def __init__(
        self,
        customer_client: CustomerClient,
    ):
        self._customer_client = customer_client

    async def submit(
        self,
        state: InvestmentState,
    ) -> GatewayResult[None]:

        goal = cast(
            UpdateFatcaExecutionGoal,
            state.goal,
        )

        return await self._customer_client.update_fatca(
            trace_id=state.trace_id,
            request=RequestContext(**asdict(state.request)),
            goal=goal,
        )