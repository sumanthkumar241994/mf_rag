import sre_compile
from typing import Any
import httpx

from app.core.config import settings
from app.core.middleware.request_context_vars import correlation_id_ctx

from app.infrastructure.api_client.base_client import BaseApiClient
from app.infrastructure.api_client.constants import DEFAULT_CONNECTION_LIMITS, DEFAULT_KEEPALIVE_CONNECTIONS, DEFAULT_TIMEOUT
from app.infrastructure.api_client.exceptions import (
    AuthenticationError,
    AuthorizationError,
    HttpClientError,
    RequestTimeoutError,
    ResourceNotFoundError,
    ServiceUnavailableError,
    ValidationError
)

from app.infrastructure.api_client.models import RequestOptions


class RestApiClient(BaseApiClient):

    def __init__(
        self,
        base_url: str,
        timeout: float = DEFAULT_TIMEOUT,
        default_headers: dict[str, str] | None = None 
    ) -> None:
        self._client = httpx.AsyncClient(
            base_url=base_url,
            timeout=timeout,
            headers=default_headers,
            limits=httpx.Limits(
                max_connections=DEFAULT_CONNECTION_LIMITS,
                max_keepalive_connections=DEFAULT_KEEPALIVE_CONNECTIONS
            )
        )
    
    async def get(self, url: str, options: RequestOptions | None = None ) -> dict[str, Any]:
        response = await self._request(
            method='GET',
            url=url,
            options=options
        )

        return response.json()

    async def post(self, url: str, body: Any | None = None, options: RequestOptions | None = None ) -> dict[str, Any]:
        response = await self._request(
            method='POST',
            url=url,
            json=body,
            options=options
        )

        return response.json()


    async def put(self, url: str, body: Any | None = None, options: RequestOptions | None = None ) -> dict[str, Any]:
        response = await self._request(
            method='PUT',
            url=url,
            json=body,
            options=options
        )

        return response.json()


    async def delete(self, url: str, options: RequestOptions | None = None ) -> dict[str, Any]:
        response = await self._request(
            method='DELETE',
            url=url,
            options=options
        )

        return response.json()

    async def close(self) -> None:
        await self._client.aclose()


    async def _request(
        self,
        method: str,
        url: str,
        options: RequestOptions | None = None,
        body: Any | None = None,
        **kwargs: Any,
    ) -> httpx.Response:

        options = options or RequestOptions()
        headers = self._build_headers(options)
        timeout = options.timeout if options.timeout is not None else DEFAULT_TIMEOUT

        try:
            response = await self._client.request(
                method=method,
                url=url,
                params=options.params,
                headers=headers,
                timeout=timeout,
                **kwargs
            )
        except httpx.TimeoutException as ex:
            raise RequestTimeoutError() from ex
        except httpx.ConnectError as ex:
            raise ServiceUnavailableError(
                message="Unable to connect to remote service."
            ) from ex
        except httpx.HTTPError as ex:
            raise HttpClientError(status_code=response.status_code, message=str(ex)) from ex
        
        self._raise_for_status(response)

        return response


    @staticmethod
    def _build_headers(options: RequestOptions) -> dict[str, str]:
        headers = dict(options.headers)

        correlation_id = correlation_id_ctx.get()
        
        if correlation_id:
            headers['X-Correlation-Id'] = str(correlation_id)
        
        if options.context.trace_id:
            headers['X-Trace-Id'] = str(options.context.trace_id)
        
        if options.context.conversation_id:
            headers['X-Conversation-Id'] = str(options.context.conversation_id)

        headers['X-Karat-Api-Key'] = settings.X_KARAT_API_KEY
        headers['Api-Key'] = settings.X_API_KEY

        return headers

    @staticmethod
    def _raise_for_status(response: httpx.Response) -> None:
        status_code = response.status_code

        if status_code == 401:
            raise AuthenticationError()
        
        elif status_code == 403:
            raise AuthorizationError()
        
        elif status_code == 404:
            raise ResourceNotFoundError()

        elif status_code == 422:
            raise ValidationError()
        
        elif status_code >= 500:
            raise ServiceUnavailableError()
        
        response.raise_for_status()


