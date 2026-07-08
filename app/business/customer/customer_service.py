from app.business.advisor.models.advisor_error import AdvisorError
from app.business.common.models.gateway_result import GatewayResult
from app.business.customer.gateway.customer_gateway import CustomerGateway
from app.business.customer.mapper.customer_mapper import CustomerMapper
from app.business.customer.models.customer import Customer
from app.infrastructure.api_client.models import GateWayRequestContext
from app.workflows.advisor.advisor_state import AdvisorState


class CustomerService:

    def __init__(
        self,
        customer_gateway: CustomerGateway,
        customer_mapper: CustomerMapper,
    ):
        self._customer_gateway = customer_gateway
        self._customer_mapper = customer_mapper

    async def retrieve(
        self,
        state: AdvisorState,
    ):
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

        state.customer = customer