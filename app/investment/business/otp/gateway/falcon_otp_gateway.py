from typing import Any
from app.infrastructure.api_client.base_client import BaseApiClient
from app.infrastructure.api_client.models import GateWayRequestContext, RequestOptions
from app.infrastructure.api_client.exceptions import (
    AuthenticationError,
    AuthorizationError,
    RequestTimeoutError,
    ResourceNotFoundError,
    ServiceUnavailableError,
    ValidationError,
)
from app.investment.base.models import GatewayResult
from app.investment.business.otp.gateway.otp_gateway import VerificationGateway
from app.investment.common.enums.gateway_error import GatewayErrorCode


class FalconOTPVerificationGateway(VerificationGateway):
    VERIFICATION_ENDPOINT = "/v4/otp_verification"
    def __init__(self, api_client: BaseApiClient):
        self._api_client = api_client

    
    async def send_otp(self, context: GateWayRequestContext, payload: dict[str, Any]) -> GatewayResult[dict[str, Any]]:
        try:
            response = await self._api_client.post(
                url=self.VERIFICATION_ENDPOINT,
                body=payload,
                options=RequestOptions(
                    context=context,
                ),
            )

            return GatewayResult.ok(response)

        except Exception as ex:
            return self._handle_exception(ex, operation='send otp')

    async def verify_otp(self, context: GateWayRequestContext, payload: dict[str, Any]) -> GatewayResult[dict[str, Any]]:
        try:
            response = await self._api_client.post(
                url=self.VERIFICATION_ENDPOINT,
                body=payload,
                options=RequestOptions(
                    context=context,
                ),
            )

            return GatewayResult.ok(response)

        except Exception as ex:
            return self._handle_exception(ex, operation='Verify otp')

    
    def _handle_exception(
        self,
        ex: Exception,
        operation: str,
    ) -> GatewayResult:

        if isinstance(ex, ResourceNotFoundError):
            return GatewayResult.failure(
                code=GatewayErrorCode.CUSTOMER_NOT_FOUND,
                message="No matching customer found.",
            )

        if isinstance(ex, ValidationError):
            return GatewayResult.failure(
                code=GatewayErrorCode.VALIDATION_ERROR,
                message=str(ex),
            )

        if isinstance(ex, AuthenticationError):
            return GatewayResult.failure(
                code=GatewayErrorCode.AUTHENTICATION_FAILED,
                message="Authentication with otp service failed.",
            )

        if isinstance(ex, AuthorizationError):
            return GatewayResult.failure(
                code=GatewayErrorCode.AUTHORIZATION_FAILED,
                message="Authorization with otp service failed.",
            )

        if isinstance(ex, RequestTimeoutError):
            return GatewayResult.failure(
                code=GatewayErrorCode.REQUEST_TIMEOUT,
                message="otp service did not respond in time.",
                retryable=True,
            )

        if isinstance(ex, ServiceUnavailableError):
            return GatewayResult.failure(
                code=GatewayErrorCode.SERVICE_UNAVAILABLE,
                message="otp service is temporarily unavailable.",
                retryable=True,
            )

        return GatewayResult.failure(
            code=GatewayErrorCode.UNKNOWN_ERROR,
            message=f"Unexpected error while attempting to {operation}: {str(ex)}",
            retryable=True,
        )