from typing import Any

from app.infrastructure.api_client.models import GateWayRequestContext
from app.investment.base.models import GatewayResult



class VerificationGateway:

    async def send_otp(
        self,
        context: GateWayRequestContext,
        payload: dict[str, Any],
    ) -> GatewayResult[dict]:
        ...

    async def verify_otp(
        self,
        context: GateWayRequestContext,
        payload: dict[str, Any],
    ) -> GatewayResult[dict]:
        ...