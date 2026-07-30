import re
from app.business.advisor.enums.capabilities import Capability
from app.business.common.models.gateway_result import GatewayResult
from app.infrastructure.api_client.models import GateWayRequestContext
from app.investment.base.models import WorkflowError
from app.investment.business.customer.gateway.customer_gateway import CustomerGateway
from app.investment.business.customer.mapper.customer_mapper import CustomerMapper
from app.investment.business.customer.models.customer import Customer
from app.investment.business.customer.models.retrieval_customer_request import RetrieveCustomerRequest
from app.investment.common.services.base_workflow_service import BaseWorkflowService
from app.investment.workflows.investment_state import InvestmentState
from app.observability.tracing import trace_step
from app.workflows.workflow.models.workflow_execution import WorkflowExecution
from app.workflows.workflow.service.workflow_service import WorkflowService


class CustomerService(BaseWorkflowService[Customer]):

    def __init__(
        self,
        customer_gateway: CustomerGateway,
        customer_mapper: CustomerMapper,
        workflow_service: WorkflowService,
    ):
        super().__init__(workflow_service)
        self._customer_gateway = customer_gateway
        self._customer_mapper = customer_mapper

    @trace_step(
        "customer_service",
        output_mapper=lambda result: {
            "success": result.success,
            "interrupted": (
                result.data.interrupted
                if result.success and result.data is not None
                else False
            ),
        },
        metadata_mapper=lambda _: {
            "service": "customer",
        },
    )
    async def retrieve(
        self,
        request: RetrieveCustomerRequest,
    ) -> GatewayResult[WorkflowExecution[Customer]] :
        """
        Retrieves customer information from the customer gateway,
        maps it into the Investment Customer domain model and
        stores it in the workflow state.
        """

        gateway_context = GateWayRequestContext(
            trace_id=request.trace_id,
            conversation_id=request.request.conversation_id,
            customer_id=request.request.customer_id,
        )

        result: GatewayResult[dict] = await self._customer_gateway.get_customer(context=gateway_context)

        if not result.success:
            return GatewayResult.failure(code=result.error.code.value,message=result.error.message)

        customer = self._customer_mapper.map(result.data)

        execution = self.create_workflow_execution(
            capability=Capability.CUSTOMER,
            result=customer,
            completed=True,
        )

        return GatewayResult.ok(execution)