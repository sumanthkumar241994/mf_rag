
from fastmcp import FastMCP
from app.mcp.client.customer_client import CustomerClient


class BusinessClientComposition:

    def __init__(self, mcp: FastMCP):
        self.customer = CustomerClient(mcp)