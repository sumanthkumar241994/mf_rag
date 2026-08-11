from dataclasses import asdict
from app.cache import customer_cache
from app.cache.customer_cache import CustomerCache
from app.investment.base.models import GatewayResult, RequestContext
from app.investment.business.customer.models.retrieval_customer_request import (
    RetrieveCustomerRequest,
)
from app.investment.common.enums.customer_state import CustomerState
from app.investment.workflows.investment_state import (
    InvestmentState,
)
from app.mcp.client.customer_client import CustomerClient


class CustomerRefreshService:

    def __init__(
        self,
        customer_client: CustomerClient,
        customer_cache: CustomerCache
    ):
        self._customer_client = customer_client
        self._customer_cache = customer_cache

    async def refresh(
        self,
        state: InvestmentState,
    ) -> GatewayResult[None]:
        await self._customer_cache.delete(state.request.customer_id)
        result = await self._customer_client.retrieve_customer(
            trace_id=state.trace_id,
            request=RequestContext(**asdict(state.request)),
        )

        if not result.success:
            return GatewayResult(
                success=False,
                error=result.error,
            )

        execution = result.result

        state.customer = execution.result
        state.customer_state = CustomerState.FRESH

        # Derived state becomes stale after customer refresh
        state.eligibility = None

        return GatewayResult(
            success=True,
            result=None,
        )