from __future__ import annotations

from typing import Any, Type, TypeVar

from fastmcp import Client
from pydantic import BaseModel

T = TypeVar("T", bound=BaseModel)


class MCPClient:
    """
    Wrapper around FastMCP Client.

    Responsibilities:
    - Manage a single MCP connection for the application's lifetime.
    - Execute MCP tools.
    - Deserialize responses.
    - Hide FastMCP implementation details.
    """

    def __init__(self, client: Client) -> None:
        self._client = client
        self._connected = False

    @property
    def is_connected(self) -> bool:
        return self._connected

    async def startup(self) -> None:
        """
        Establish the MCP connection.

        Safe to call multiple times.
        """
        if self._connected:
            return

        await self._client.__aenter__()
        self._connected = True

    async def shutdown(self) -> None:
        """
        Close the MCP connection.

        Safe to call multiple times.
        """
        if not self._connected:
            return

        await self._client.__aexit__(None, None, None)
        self._connected = False

    async def call(
        self,
        *,
        tool_name: str,
        request: BaseModel,
        response_model: type[T],
    ) -> Any:
        """
        Invoke an MCP tool and deserialize the response.
        """
        if not self._connected:
            raise RuntimeError(
                "MCP client has not been started. Call startup() during application startup."
            )

        request = request.model_dump(mode="json")

        result = await self._client.call_tool(
            tool_name,
            request,
        )

        return response_model.model_validate(
            result.structured_content
        )