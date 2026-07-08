from app.business.portfolio.gateways.portfolio_gateway import PortfolioGateway
from app.business.portfolio.mapper.portfolio_mapper import PortfolioMapper
from app.business.portfolio.models import Portfolio, portfolio
from app.business.common.enums.gateway_error import GatewayErrorCode
from app.infrastructure.api_client.base_client import BaseApiClient
from app.infrastructure.api_client.exceptions import (
    AuthenticationError,
    AuthorizationError,
    RequestTimeoutError,
    ResourceNotFoundError,
    ServiceUnavailableError,
    ValidationError
)

from app.infrastructure.api_client.models import RequestOptions, GateWayRequestContext
from app.business.common.models.gateway_result import GatewayResult
from app.infrastructure.api_client.rest_client import RestApiClient


class FalconPortfolioGateway(PortfolioGateway):
    PORTFOLIO_END_POINT = "/v2/local/investments"

    def __init__(self, api_client: RestApiClient) -> None:
        self.api_client = api_client

    async def get_portfolio(self,  context: GateWayRequestContext | None = None) -> GatewayResult[Portfolio]:
        try:
            response = await self.api_client.get(
                url=self.PORTFOLIO_END_POINT,
                options=RequestOptions(
                    context=context
                )
            )

            return GatewayResult.ok(response)

        except ResourceNotFoundError:
            return GatewayResult.failure(
                code=GatewayErrorCode.PORTFOLIO_NOT_FOUND,
                message='Portfolio service is temporarily unavailable.',
            )

        except ValidationError as ex:
            return GatewayResult.failure(
                code=GatewayErrorCode.VALIDATION_ERROR,
                message=str(ex)
            )
        
        except AuthenticationError:
            return GatewayResult.failure(
                code=GatewayErrorCode.AUTHENTICATION_FAILED,
                message="Authentication with portfolio service failed.",
            )

        except AuthorizationError:
            return GatewayResult.failure(
                code=GatewayErrorCode.AUTHORIZATION_FAILED,
                message="Authorization with portfolio service failed."
            )

        except RequestTimeoutError:
            return GatewayResult.failure(
                code=GatewayErrorCode.REQUEST_TIMEOUT,
                message='Portfolio service did not respond in time.',
                retryable=True
            )
        
        except  ServiceUnavailableError:
            return GatewayResult.failure(
                code=GatewayErrorCode.SERVICE_UNAVAILABLE,
                message='Portfolio service is temporarily unavailable.',
                retryable=True
            )
        
        except Exception as ex:
            return GatewayResult.failure(
                code=GatewayErrorCode.UNKNOWN_ERROR,
                message=f'Unexpected error while retrieving portfolio. {str(ex)}',
                retryable=True
            )