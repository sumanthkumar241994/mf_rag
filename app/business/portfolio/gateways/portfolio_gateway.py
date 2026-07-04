from abc import ABC, abstractmethod
from app.business.portfolio.models import Portfolio
from app.business.common.models.gateway_result import GatewayResult
from app.infrastructure.api_client.models import GateWayRequestContext


class PortfolioGateway(ABC):

    @abstractmethod
    async def get_portfolio(self, context: GateWayRequestContext | None = None) -> GatewayResult[Portfolio]:
        raise NotImplementedError