from app.business.customer.gateway.falcon_customer_gateway import FalconCustomerGateway
from app.core.config import settings
from app.infrastructure.api_client.rest_client import RestApiClient

def get_customer_gateway() -> FalconCustomerGateway:
    return FalconCustomerGateway(RestApiClient(base_url=settings.MF_API_BASE_URL))
