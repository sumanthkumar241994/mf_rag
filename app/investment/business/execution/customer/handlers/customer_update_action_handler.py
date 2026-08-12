from abc import ABC, abstractmethod

from app.investment.base.models import GatewayResult, WorkflowError
from app.investment.business.customer.models.customer import Customer
from app.investment.business.execution.action_handler import ActionHandler
from app.investment.models.action_type import NextAction
from app.investment.models.execution_result import ExecutionResult, ExecutionStatus
from app.investment.workflows.investment_state import InvestmentState
from app.workflows.workflow.models.workflow_execution import (
    WorkflowExecution,
)


class CustomerUpdateActionHandler(ActionHandler, ABC):

    async def execute(
        self,
        state: InvestmentState,
        action: NextAction
    ) -> ExecutionResult:

        result = await self.submit(state)

        if not result.success:
            error = WorkflowError.from_gateway(error=result.error, source="Customer gateway")
            state.add_error(error)
            return ExecutionResult(status=ExecutionStatus.FAILED, execution=execution)

        execution = result.data

        state.customer = execution.result

        # Customer has changed, invalidate any derived state.
        state.eligibility = None

        if state.workflow_execution is not None:
            state.workflow_execution.interrupt = None

        await self.after_update(state)

        return ExecutionResult(status=ExecutionStatus.COMPLETED, execution=execution)
        
    async def after_update(
        self,
        state: InvestmentState,
    ) -> None:
        """
        Hook for subclasses.

        Override only if additional processing is required
        after updating the customer.
        """
        return None

    @abstractmethod
    async def submit(
        self,
        state: InvestmentState,
    ) -> GatewayResult[WorkflowExecution[Customer]]:
        """
        Execute the customer update.

        Examples:
        - Update Nominee
        - Update Bank
        - Update FATCA
        - Update Signature
        """
        raise NotImplementedError