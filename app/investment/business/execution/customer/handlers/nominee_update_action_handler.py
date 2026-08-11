from dataclasses import asdict
from typing import cast

from app.investment.base.models import GatewayResult, RequestContext
from app.investment.business.execution.customer.handlers.customer_update_action_handler import CustomerUpdateActionHandler
from app.investment.business.execution.goal.update_nominee_execution_goal import UpdateNomineeExecutionGoal
from app.investment.common.services.customer_refresh_service import CustomerRefreshService
from app.investment.workflows.investment_state import (
    InvestmentState,
)
from app.mcp.client.customer_client import CustomerClient


class NomineeUpdateActionHandler(CustomerUpdateActionHandler):

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
            UpdateNomineeExecutionGoal,
            state.goal,
        )

        return await self._customer_client.update_nominee(
            trace_id=state.trace_id,
            request=RequestContext(**asdict(state.request)),
            goal=goal
        )