from abc import ABC, abstractmethod

from app.investment.base.models import GatewayResult
from app.investment.business.customer.models.customer import Customer
from app.investment.business.execution.action_handler import ActionHandler
from app.investment.workflows.investment_state import InvestmentState
from app.workflows.workflow.models.workflow_execution import (
    WorkflowExecution,
)


class CustomerUpdateActionHandler(ActionHandler, ABC):

    async def execute(
        self,
        state: InvestmentState,
    ) -> None:

        result = await self.submit(state)

        if not result.success:
            state.add_error(result.error)
            return

        execution = result.result

        state.customer = execution.result

        # Customer has changed, invalidate any derived state.
        state.eligibility = None

        await self.after_update(state)

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