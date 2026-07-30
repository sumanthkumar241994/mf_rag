from fastmcp import Client

from app.mcp.client.mcp_client import MCPClient


class MCPComposition:

    def __init__(self):
        self.client = MCPClient(Client("http://localhost:8001/mcp"))