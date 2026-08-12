

from dataclasses import asdict
from app.investment.base.models import RequestContext, WorkflowError
from app.investment.business.execution.action_handler import ActionHandler
from app.investment.common.enums.action_type import ActionType
from app.investment.common.enums.customer_state import CustomerState
from app.investment.models.action_type import NextAction
from app.investment.models.execution_result import ExecutionResult, ExecutionStatus
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
    ) -> ExecutionResult:

        if action.action != ActionType.CHECK_CUSTOMER:
            raise ValueError(
                f"Unsupported action '{action.action.value}' "
                f"for {self.__class__.__name__}"
            )
        return await self._check_customer(state)

    async def _check_customer(
        self,
        state: InvestmentState,
    ) -> ExecutionResult:

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
            return ExecutionResult(status=ExecutionStatus.FAILED, execution=None)

        execution = result.data

        state.workflow_execution = execution
        state.customer = execution.result
        state.customer_state = CustomerState.FRESH

        return ExecutionResult(status=ExecutionStatus.CONTINUE, execution=execution)