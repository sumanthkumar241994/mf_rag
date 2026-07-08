from app.business.scheme.gateways.falcon_scheme_gateway import FalconSchemeGateway
from app.core.config import settings
from app.infrastructure.api_client.rest_client import RestApiClient

def get_scheme_gateway() -> FalconSchemeGateway:
    return FalconSchemeGateway(RestApiClient(base_url=settings.MF_API_BASE_URL))
