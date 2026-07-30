from abc import ABC, abstractmethod
from typing import Any

from app.business.common.models.gateway_result import GatewayResult
from app.infrastructure.api_client.models import GateWayRequestContext


class CustomerGateway(ABC):

    @abstractmethod
    async def get_customer(
        self,
        context: GateWayRequestContext | None = None
    ) -> GatewayResult[dict[str, Any]]:
        """
        Retrieve customer information.
        """
        raise NotImplementedError