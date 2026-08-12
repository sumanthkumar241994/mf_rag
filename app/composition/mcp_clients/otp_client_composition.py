from app.mcp.client.mcp_client import MCPClient
from app.mcp.client.otp_client import OTPClient


class OTPClientComposition:

    def __init__(self, mcp: MCPClient):
        self.client = OTPClient(mcp)