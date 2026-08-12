
from fastmcp import FastMCP
from app.api.dependencies.rest_api_client import get_rest_api_client
from app.composition.business.new_customer_composition import NewCustomerComposition
from app.composition.business.otp_composition import OTPVerificationComposition
from app.core.config.redis import get_redis


redis = get_redis()
rest_api_client = get_rest_api_client()

# MCP server
mcp = FastMCP("Mutual Fund Business Services")

customer = NewCustomerComposition(
        redis=redis,
        rest_api_client=rest_api_client,
    )

otp = OTPVerificationComposition(rest_api_client=rest_api_client)

otp.register_mcp(mcp)
customer.register_mcp(mcp)

app = mcp.http_app()