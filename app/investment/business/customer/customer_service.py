import re
from app.business.common.models.gateway_result import GatewayResult
from app.infrastructure.api_client.models import GateWayRequestContext
from app.investment.business.customer.gateway.customer_gateway import CustomerGateway
from app.investment.business.customer.mapper.customer_mapper import CustomerMapper
from app.investment.business.customer.models.customer import Customer
from app.investment.business.customer.models.retrieval_customer_request import RetrieveCustomerRequest
from app.investment.business.customer.models.update_fatca_request import UpdateFatcaRequest
from app.investment.business.customer.models.update_nominee_request import UpdateNomineeRequest
from app.investment.workflows.models.workflow_execution import WorkflowExecution
from app.observability.tracing import trace_step


class CustomerService:

    def __init__(
        self,
        customer_gateway: CustomerGateway,
        customer_mapper: CustomerMapper,
    ):
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

        execution = WorkflowExecution(
            result=customer,
        )

        return GatewayResult.ok(execution)
    
    async def update_nominee(
    self,
    request: UpdateNomineeRequest,
    ) -> GatewayResult[WorkflowExecution[Customer]]:

        gateway_context = GateWayRequestContext(
            trace_id=request.trace_id,
            conversation_id=request.request.conversation_id,
            customer_id=request.request.customer_id,
        )

        result = await self._customer_gateway.update_nominee(
            context=gateway_context,
            nominee=request.goal.nominee,
            verification_id=request.verification_id
        )

        if not result.success:
            return GatewayResult.failure(
                code=result.error.code,
                message=result.error.message,
            )

        customer = self._customer_mapper.map(
            result.data,
        )

        execution = WorkflowExecution(
            result=customer,
        )

        return GatewayResult.ok(execution)


    async def update_fatca(
    self,
    request: UpdateFatcaRequest,
    ) -> GatewayResult[WorkflowExecution[Customer]]:

        gateway_context = GateWayRequestContext(
            trace_id=request.trace_id,
            conversation_id=request.request.conversation_id,
            customer_id=request.request.customer_id,
        )

        result = await self._customer_gateway.update_fatca(
            context=gateway_context,
            fatca=request.goal.fatca,
        )

        if not result.success:
            return GatewayResult.failure(
                code=result.error.code,
                message=result.error.message,
            )

        customer = self._customer_mapper.map(
            result.data,
        )

        execution = WorkflowExecution(
            result=customer,
        )

        return GatewayResult.ok(execution)