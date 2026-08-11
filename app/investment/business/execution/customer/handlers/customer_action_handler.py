

from dataclasses import asdict
from app.investment.base.models import RequestContext, WorkflowError
from app.investment.business.execution.action_handler import ActionHandler
from app.investment.common.enums.action_type import ActionType
from app.investment.common.enums.customer_state import CustomerState
from app.investment.models.action_type import NextAction
from app.investment.workflows.investment_state import InvestmentState
from app.mcp.client.customer_client import CustomerClient


class CustomerActionHandler(ActionHandler):

    def __init__(
        self,
        customer_client: CustomerClient,
    ):
        self._customer_client = customer_client

    async def execute(
        self,
        state: InvestmentState,
        action: NextAction,
    ) -> None:

        if action.action != ActionType.CHECK_CUSTOMER:
            raise ValueError(
                f"Unsupported action '{action.action.value}' "
                f"for {self.__class__.__name__}"
            )
        await self._check_customer(state)

    async def _check_customer(
        self,
        state: InvestmentState,
    ) -> None:

        result = await self._customer_client.retrieve_customer(
            trace_id=state.trace_id,
            request=RequestContext(**asdict(state.request)),
        )

        if not result.success:
            state.add_error(
                WorkflowError.from_gateway(
                    error=result.error,
                    source="customer_gateway",
                )
            )
            return

        execution = result.data

        state.workflow_execution = execution
        state.customer = execution.result
        state.customer_state = CustomerState.FRESH