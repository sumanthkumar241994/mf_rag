# app/mcp/manager.py

from fastmcp import Client, FastMCP

from app.composition.business.new_customer_composition import NewCustomerComposition


class MCPManager:

    def __init__(
        self,
        customer: NewCustomerComposition,
    ) -> None:
        self._customer = customer

        self.server = FastMCP(
            name="Mutual Fund Business Services",
        )

        self.client: Client | None = None

    async def startup(self) -> None:
        """
        Register all business modules with the MCP server and
        initialize the shared MCP client.
        """

        # Register Customer tools
        self._customer.register_mcp(
            mcp=self.server,
        )

        # Future
        # self._portfolio_composition.register_mcp(self.server)
        # self._order_composition.register_mcp(self.server)
        # self._nominee_composition.register_mcp(self.server)

        self.client = Client(self.server)

        await self.client.__aenter__()

    async def shutdown(self) -> None:
        if self.client:
            await self.client.__aexit__(None, None, None)