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
from app.investment.business.customer.gateway.customer_gateway import CustomerGateway
from app.investment.business.customer.models.fatca import Fatca
from app.investment.business.customer.models.nominee import Nominee
from app.investment.common.enums.gateway_error import GatewayErrorCode


class FalconCustomerGateway(CustomerGateway):
    CUSTOMER_ENDPOINT = "/v2/customer/me"
    def __init__(self, api_client: BaseApiClient):
        self._api_client = api_client

    
    async def get_customer(self, context: GateWayRequestContext | None = None ) -> GatewayResult[dict[str, Any]]:
        try:
            response = await self._api_client.get(
                url=self.CUSTOMER_ENDPOINT,
                options=RequestOptions(
                    context=context,
                ),
            )

            return GatewayResult.ok(response)

        except Exception as ex:
            return self._handle_exception(ex, operation='retrieve customer')

    async def update_nominee(self, nominee: Nominee, context: GateWayRequestContext | None = None) -> GatewayResult[dict[str, Any]]:
        try:
            response = await self._api_client.post(
                url=self.CUSTOMER_ENDPOINT,
                body=nominee.model_dump(mode='json'),
                options=RequestOptions(
                    context=context,
                ),
            )

            return GatewayResult.ok(response)

        except Exception as ex:
            return self._handle_exception(ex, operation='update nominee')

    async def update_fatca(self, fatca: Fatca, context: GateWayRequestContext | None = None) -> GatewayResult[dict[str, Any]]:
        try:
            response = await self._api_client.post(
                url=self.CUSTOMER_ENDPOINT,
                body=fatca.model_dump(mode='json'),
                options=RequestOptions(
                    context=context,
                ),
            )

            return GatewayResult.ok(response)

        except Exception as ex:
            return self._handle_exception(ex, operation='update fatca')

    
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
                message="Authentication with customer service failed.",
            )

        if isinstance(ex, AuthorizationError):
            return GatewayResult.failure(
                code=GatewayErrorCode.AUTHORIZATION_FAILED,
                message="Authorization with customer service failed.",
            )

        if isinstance(ex, RequestTimeoutError):
            return GatewayResult.failure(
                code=GatewayErrorCode.REQUEST_TIMEOUT,
                message="customer service did not respond in time.",
                retryable=True,
            )

        if isinstance(ex, ServiceUnavailableError):
            return GatewayResult.failure(
                code=GatewayErrorCode.SERVICE_UNAVAILABLE,
                message="Customer service is temporarily unavailable.",
                retryable=True,
            )

        return GatewayResult.failure(
            code=GatewayErrorCode.UNKNOWN_ERROR,
            message=f"Unexpected error while attempting to {operation}: {str(ex)}",
            retryable=True,
        )