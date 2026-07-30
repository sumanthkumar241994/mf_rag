from fastmcp import FastMCP
from redis.asyncio import Redis
from app.business.customer.gateway.cached_customer_gateway import CachedCustomerGateway
from app.business.customer.gateway.falcon_customer_gateway import FalconCustomerGateway
from app.cache.customer_cache import CustomerCache
from app.core.config import settings
from app.infrastructure.api_client.rest_client import RestApiClient
from app.investment.business.customer.customer_service import CustomerService
from app.investment.business.customer.mapper import customer_mapper
from app.investment.business.customer.mapper.customer_mapper import CustomerMapper
from app.mcp.tools.customer import register_customer_tools
from app.workflows.workflow.service.workflow_service import WorkflowService


class NewCustomerComposition:

    def __init__(
        self,
        redis: Redis,
        rest_api_client: RestApiClient
    ):
        self._gateway = CachedCustomerGateway(
            customer_gateway=FalconCustomerGateway(rest_api_client),
            customer_cache=CustomerCache(redis)
            )
        
        self._workflow_service = WorkflowService()
        self._customer_mapper = CustomerMapper()

        self.customer_service = CustomerService(
            customer_gateway=self._gateway,
            customer_mapper=self._customer_mapper,
            workflow_service=self._workflow_service
        )

    def register_mcp(self, mcp: FastMCP) -> None:
        register_customer_tools(
            mcp=mcp, 
            customer_service=self.customer_service,
        )