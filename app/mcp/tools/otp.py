# app/mcp/tools/otp.py

from fastmcp import FastMCP

from app.investment.base.models import GatewayResult
from app.investment.business.otp.models.verification_request import VerificationRequest
from app.investment.business.otp.models.verification_result import SendOTPResult, VerifyOTPResult
from app.investment.business.otp.otp_service import OTPVerificationService


def register_otp_tools(mcp: FastMCP, otp_service: OTPVerificationService) -> None:
    """
    Registers otp-related MCP tools.
    """

    @mcp.tool(name="send_otp", description="Send otp to authorize the request")
    async def send_otp(request: VerificationRequest) -> GatewayResult[SendOTPResult]:
        return await otp_service.send_otp(request)

    @mcp.tool(name="verify_otp", description="verify otp to authorize the request")
    async def send_otp(request: VerificationRequest) -> GatewayResult[VerifyOTPResult]:
        return await otp_service.verify_otp(request)