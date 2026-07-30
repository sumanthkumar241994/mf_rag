
from app.mcp.client.mcp_client import MCPClient


_mcp: MCPClient | None = None


def initialize_mcp(client: MCPClient) -> None:
    global _mcp
    _mcp = client


def get_mcp() -> MCPClient:
    if _mcp is None:
        raise RuntimeError("MCP has not been initialized.")

    return _mcp