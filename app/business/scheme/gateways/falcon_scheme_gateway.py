from typing import Any
from app.business.common.enums.gateway_error import GatewayErrorCode
from app.business.common.models.gateway_result import GatewayResult
from app.business.scheme.gateways.scheme_gateway import SchemeGateway
from app.business.scheme.models.scheme_query import SchemeQuery
from app.infrastructure.api_client.base_client import BaseApiClient
from app.infrastructure.api_client.exceptions import ResourceNotFoundError
from app.infrastructure.api_client.models import GateWayRequestContext, RequestOptions
from app.infrastructure.api_client.exceptions import (
    AuthenticationError,
    AuthorizationError,
    RequestTimeoutError,
    ResourceNotFoundError,
    ServiceUnavailableError,
    ValidationError,
)


class FalconSchemeGateway(SchemeGateway):
    SCHEME_SEARCH_ENDPOINT = "/v1/local/schemes"
    SCHEME_DETAILS_ENDPOINT = "/v1/local/scheme/{scheme_id}"
    def __init__(self, api_client: BaseApiClient):
        self._api_client = api_client
    
    async def search(self, request: SchemeQuery, context: GateWayRequestContext | None = None) -> GatewayResult[list[dict[str, Any]]]:
        try:
            response = await self._api_client.get(
                url = self.SCHEME_SEARCH_ENDPOINT,
                options = RequestOptions(
                    context=context,
                    params=self._build_search_params(request)
                )
            )

            return GatewayResult.ok(response)

        except Exception as ex:
            return self._handle_exception(ex, operation='search schemes')

    
    async def get_scheme_details(self, scheme_id: int, context: GateWayRequestContext | None = None ) -> GatewayResult[dict[str, Any]]:
        try:
            response = await self._api_client.get(
                url=self.SCHEME_DETAILS_ENDPOINT.format(
                    scheme_id=scheme_id
                ),
                options=RequestOptions(
                    context=context,
                ),
            )

            return GatewayResult.ok(response)

        except Exception as ex:
            return self._handle_exception(ex, operation='retrieve scheme details')

    
    def _build_search_params(
        self,
        request: SchemeQuery,
    ) -> dict[str, Any]:

        params: dict[str, Any] = {
            "page": request.page,
            "limit": request.max_results,
            "sort": request.sort.value,
        }

        if request.q:
            params["q"] = request.q
        elif request.scheme_names:
            params["q"] = ",".join(request.scheme_names)

        if request.categories:
            params["categories"] = ",".join(request.categories)

        if request.scheme_types:
            params["scheme_type"] = ",".join(request.scheme_types)

        if request.amc_names:
            params["amc_name"] = ",".join(request.amc_names)

        if request.rating:
            params["rating"] = request.rating

        if request.riskometer:
            params["riskometer"] = request.riskometer

        if request.investment_option:
            params["investment_option"] = request.investment_option

        return params

    
    def _handle_exception(
        self,
        ex: Exception,
        operation: str,
    ) -> GatewayResult:

        if isinstance(ex, ResourceNotFoundError):
            return GatewayResult.failure(
                code=GatewayErrorCode.SCHEME_NOT_FOUND,
                message="No matching schemes found.",
            )

        if isinstance(ex, ValidationError):
            return GatewayResult.failure(
                code=GatewayErrorCode.VALIDATION_ERROR,
                message=str(ex),
            )

        if isinstance(ex, AuthenticationError):
            return GatewayResult.failure(
                code=GatewayErrorCode.AUTHENTICATION_FAILED,
                message="Authentication with scheme service failed.",
            )

        if isinstance(ex, AuthorizationError):
            return GatewayResult.failure(
                code=GatewayErrorCode.AUTHORIZATION_FAILED,
                message="Authorization with scheme service failed.",
            )

        if isinstance(ex, RequestTimeoutError):
            return GatewayResult.failure(
                code=GatewayErrorCode.REQUEST_TIMEOUT,
                message="Scheme service did not respond in time.",
                retryable=True,
            )

        if isinstance(ex, ServiceUnavailableError):
            return GatewayResult.failure(
                code=GatewayErrorCode.SERVICE_UNAVAILABLE,
                message="Scheme service is temporarily unavailable.",
                retryable=True,
            )

        return GatewayResult.failure(
            code=GatewayErrorCode.UNKNOWN_ERROR,
            message=f"Unexpected error while attempting to {operation}: {str(ex)}",
            retryable=True,
        )