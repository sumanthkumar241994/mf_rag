from app.business.advisor.enums.capabilities import Capability
from app.business.advisor.models.advisor_error import AdvisorError
from app.business.common.models.gateway_result import GatewayResult
from app.business.common.services.base_workflow_service import BaseWorkflowService
from app.business.customer.gateway.customer_gateway import CustomerGateway
from app.business.customer.mapper.customer_mapper import CustomerMapper
from app.business.customer.models.customer import Customer
from app.infrastructure.api_client.models import GateWayRequestContext
from app.workflows.advisor.advisor_state import AdvisorState
from app.workflows.workflow.models.workflow_execution import WorkflowExecution
from app.workflows.workflow.service.workflow_service import WorkflowService


class CustomerService(BaseWorkflowService[Customer]):

    def __init__(
        self,
        customer_gateway: CustomerGateway,
        customer_mapper: CustomerMapper,
        workflow_service: WorkflowService
    ):
        super().__init__(workflow_service)
        self._customer_gateway = customer_gateway
        self._customer_mapper = customer_mapper
        self._workflow_service = workflow_service

    async def retrieve(
        self,
        state: AdvisorState,
    ) -> WorkflowExecution[Customer]:
        """
        Retrieves the customer's profile information.

        The resulting Customer model is stored in AdvisorState.
        """

        gateway_context = GateWayRequestContext(
            trace_id=state.trace_id,
            conversation_id=state.request.conversation_id,
            customer_id=state.request.customer_id,
        )

        result: GatewayResult[dict] = await self._customer_gateway.get_customer(
            context=gateway_context,
        )

        if not result.success:
            state.add_error(
                AdvisorError.from_gateway(
                    error=result.error,
                    source="customer_gateway",
                )
            )
            return

        customer: Customer = self._customer_mapper.map(result.data)

        execution = self._create_workflow_execution(
            state=state,
            capability=Capability.CUSTOMER,
            result=customer,
            complete=True
        )

        state.customer = customer
        state.workflow_execution = execution

        return execution