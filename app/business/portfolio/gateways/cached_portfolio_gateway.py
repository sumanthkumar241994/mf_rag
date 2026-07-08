from typing import Any

from app.business.common.models.gateway_result import GatewayResult
from app.business.portfolio.gateways.portfolio_gateway import PortfolioGateway
from app.cache.portfolio_cache import PortfolioCache
from app.infrastructure.api_client.models import GateWayRequestContext


class CachedPortfolioGateway(PortfolioGateway):

    def __init__(
        self,
        portfolio_cache: PortfolioCache,
        portfolio_gateway: PortfolioGateway,
    ):
        self._portfolio_cache = portfolio_cache
        self._gateway = portfolio_gateway

    async def get_portfolio(
        self,
        context: GateWayRequestContext | None = None,
    ) -> GatewayResult[dict[str, Any]]:

        if context is None or context.customer_id is None:
            return await self._gateway.get_portfolio(
                context=context,
            )

        customer_id = context.customer_id

        cached = await self._portfolio_cache.get(
            customer_id,
        )

        if cached is not None:
            return GatewayResult.ok(cached)

        result = await self._gateway.get_portfolio(
            context=context,
        )

        if not result.success:
            return result

        await self._portfolio_cache.set(
            customer_id=customer_id,
            portfolio=result.data,
        )

        return result

    async def refresh(
        self,
        context: GateWayRequestContext,
    ) -> GatewayResult[dict[str, Any]]:

        result = await self._gateway.get_portfolio(
            context=context,
        )

        if not result.success:
            return result

        await self._portfolio_cache.set(
            customer_id=context.customer_id,
            portfolio=result.data,
        )

        return result

    async def invalidate(
        self,
        customer_id: str,
    ) -> None:

        await self._portfolio_cache.delete(customer_id)