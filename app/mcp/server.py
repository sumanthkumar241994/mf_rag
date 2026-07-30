
from fastmcp import FastMCP
from app.api.dependencies.rest_api_client import get_rest_api_client
from app.composition.business.new_customer_composition import NewCustomerComposition
from app.core.config.redis import get_redis


redis = get_redis()
rest_api_client = get_rest_api_client()

# MCP server
mcp = FastMCP("Mutual Fund Business Services")

customer = NewCustomerComposition(
        redis=redis,
        rest_api_client=rest_api_client,
    )

customer.register_mcp(mcp)

app = mcp.http_app()