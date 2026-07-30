from app.core.config import settings
from app.infrastructure.api_client.rest_client import RestApiClient


_rest_api_client: RestApiClient | None = None

def get_rest_api_client() -> RestApiClient:
    global _rest_api_client

    if _rest_api_client is None:
        _rest_api_client = RestApiClient(
            base_url=settings.MF_API_BASE_URL
        )

    return _rest_api_client