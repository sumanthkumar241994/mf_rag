from abc import ABC, abstractmethod
from typing import Any

from app.infrastructure.api_client.models import RequestOptions


class BaseApiClient(ABC):
    """
    Base client for communicating with external services.

    This abstraction allows different transport mechanisms
    (REST, gRPC, MCP, etc.) while exposing a common interface
    to the business layer.
    """

    @abstractmethod
    async def get(self, url: str, options: RequestOptions | None = None) -> dict[str, Any]:
        raise NotImplementedError
    
    @abstractmethod
    async def post(self, url: str, body: Any | None = None, options: RequestOptions | None = None) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    async def put(self, url: str, body: Any | None = None, options: RequestOptions | None = None) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    async def delete(self, url: str, options: RequestOptions | None = None) -> dict[str, Any]:
        raise NotImplementedError

    @abstractmethod
    async def close(self) -> None:
        """Release underlying resources"""
        raise NotImplementedError