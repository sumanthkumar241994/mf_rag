from typing import Any

from app.cache.customer_cache import CustomerCache
from app.infrastructure.api_client.models import GateWayRequestContext
from app.investment.base.models import GatewayResult
from app.investment.business.customer.gateway.customer_gateway import CustomerGateway


class CachedCustomerGateway(CustomerGateway):
    """
    Decorates CustomerGateway with Redis caching.

    Falcon remains the source of truth.
    Redis stores the raw Falcon response.
    """

    def __init__(
        self,
        customer_cache: CustomerCache,
        customer_gateway: CustomerGateway,
    ):
        self._customer_cache = customer_cache
        self._gateway = customer_gateway

    async def get_customer(
        self,
        context: GateWayRequestContext | None = None,
    ) -> GatewayResult[dict[str, Any]]:

        if context is None or context.customer_id is None:
            return await self._gateway.get_customer(context=context)

        customer_id = context.customer_id

        # ---------------------------------------------------------
        # Cache Lookup
        # ---------------------------------------------------------
        cached_response = await self._customer_cache.get(customer_id)

        if cached_response is not None:
            return GatewayResult.ok(cached_response)

        # ---------------------------------------------------------
        # Falcon Lookup
        # ---------------------------------------------------------
        result = await self._gateway.get_customer(context=context)

        if not result.success:
            return result

        # ---------------------------------------------------------
        # Cache Falcon Response
        # ---------------------------------------------------------
        await self._customer_cache.set(
            customer_id=customer_id,
            customer=result.data,
        )

        return result

    async def refresh(
        self,
        context: GateWayRequestContext,
    ) -> GatewayResult[dict[str, Any]]:
        """
        Refreshes the customer cache from Falcon.
        """

        result = await self._gateway.get_customer(context=context)

        if not result.success:
            return result

        await self._customer_cache.set(
            customer_id=context.customer_id,
            customer=result.data,
        )

        return result

    async def invalidate(
        self,
        customer_id: str,
    ) -> None:
        """
        Removes customer data from Redis.
        """

        await self._customer_cache.delete(customer_id)