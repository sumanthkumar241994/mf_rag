from app.investment.base.models import GatewayResult
from app.investment.business.otp.models.verification_request import VerificationRequest
from app.investment.business.otp.models.verification_result import SendOTPResult, VerifyOTPResult
from app.mcp.client.mcp_client import MCPClient


class OTPClient:

    def __init__(
        self,
        client: MCPClient,
    ):
        self._client = client

    async def send_otp(
        self,
        request: VerificationRequest,
    ) -> GatewayResult[SendOTPResult]:

        result = await self._client.call(
            tool_name="send_otp",
            response_model=GatewayResult[SendOTPResult],
            request=request,
        )

        # deserialize here
        return GatewayResult.model_validate(result)

    async def verify_otp(
        self,
        request: VerificationRequest,
    ) -> GatewayResult[VerifyOTPResult]:

        result = await self._client.call(
            tool_name="verify_otp",
            response_model=GatewayResult[VerifyOTPResult],
            request=request,
        )

        # deserialize here
        return GatewayResult.model_validate(result)