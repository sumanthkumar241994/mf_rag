from fastmcp import FastMCP

from app.infrastructure.api_client.rest_client import RestApiClient
from app.investment.business.otp.gateway.falcon_otp_gateway import FalconOTPVerificationGateway
from app.investment.business.otp.mapper import otp_mapper
from app.investment.business.otp.otp_service import OTPVerificationService
from app.mcp.tools.otp import register_otp_tools


class OTPVerificationComposition:

    def __init__(
        self,
        rest_api_client: RestApiClient
    ):
        self._gateway = FalconOTPVerificationGateway(rest_api_client)
        
        self._otp_mapper = otp_mapper.VerificationMapper()

        self.otp_service = OTPVerificationService(
            verification_gateway=self._gateway,
            verification_mapper=self._otp_mapper,
        )

    def register_mcp(self, mcp: FastMCP) -> None:
        register_otp_tools(
            mcp=mcp, 
            otp_service=self.otp_service,
        )