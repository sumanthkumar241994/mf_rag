from redis.asyncio import Redis
from sqlalchemy.sql.cache_key import CacheConst
from app.business.advisor.enums.capabilities import Capability
from app.business.advisor.enums.tool_type import ToolType
from app.business.customer.customer_service import CustomerService
from app.business.customer.gateway.cached_customer_gateway import CachedCustomerGateway
from app.business.customer.gateway.falcon_customer_gateway import FalconCustomerGateway
from app.business.customer.mapper.customer_mapper import CustomerMapper
from app.cache.customer_cache import CustomerCache
from app.composition.workflow_composition import WorkflowComposition
from app.infrastructure.api_client.rest_client import RestApiClient
from app.tools.definitions.tool_definition import ToolDefinition
from app.tools.implementations.customer_tool import CustomerTool
from app.workflows.workflow.service.workflow_service import WorkflowService


class CustomerComposition:

    def __init__(
        self,
        redis: Redis,
        rest_api_client: RestApiClient,
        workflow_service: WorkflowService
    ):
        self.customer_mapper = CustomerMapper()
        self.customer_gateway = CachedCustomerGateway(
            customer_cache=CustomerCache(redis),
            customer_gateway=FalconCustomerGateway(rest_api_client)
        )
        self.customer_service = CustomerService(
            customer_gateway=self.customer_gateway,
            customer_mapper=self.customer_mapper,
            workflow_service=workflow_service
        )

        self.definition = ToolDefinition(
            name=ToolType.CUSTOMER.value,
            description=(
                "Retrieve customer profile, KYC, bank, nominee, "
                "investment eligibility and onboarding information."
            ),
            capability=Capability.CUSTOMER,
            timeout_seconds=30,
            tags=[
                "customer",
                "profile",
                "kyc",
                "bank",
                "nominee",
                "risk-profile",
                "onboarding",
            ],
        )

        self.tool = CustomerTool(
            customer_service=self.customer_service,
        )