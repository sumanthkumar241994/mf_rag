from abc import ABC, abstractmethod
from typing import Any

from app.business.common.models.gateway_result import GatewayResult
from app.infrastructure.api_client.models import GateWayRequestContext
from app.investment.business.customer.models.fatca import Fatca
from app.investment.business.customer.models.nominee import Nominee


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

    @abstractmethod
    async def update_nominee(
        self,
        nominee: Nominee,
        verification_id: str,
        context: GateWayRequestContext | None = None
    ) -> GatewayResult[dict[str, Any]]:
        """
        Retrieve customer information.
        """
        raise NotImplementedError

    @abstractmethod
    async def update_fatca(
        self,
        fatca: Fatca,
        context: GateWayRequestContext | None = None
    ) -> GatewayResult[dict[str, Any]]:
        """
        Retrieve customer information.
        """
        raise NotImplementedError