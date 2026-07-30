from app.mcp.client.customer_client import CustomerClient
from app.mcp.client.mcp_client import MCPClient


class CustomerClientComposition:

    def __init__(self, mcp: MCPClient):
        self.client = CustomerClient(mcp)