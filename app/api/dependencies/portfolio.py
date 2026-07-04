from app.business.portfolio.gateways.falcon_portfolio_gateway import FalconPortfolioGateway
from app.core.config import settings
from app.infrastructure.api_client.rest_client import RestApiClient

def get_portfolio_gateway() -> FalconPortfolioGateway:
    return FalconPortfolioGateway(RestApiClient(base_url=settings.MF_API_BASE_URL))
