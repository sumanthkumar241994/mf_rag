from fastapi import Depends
from redis.asyncio import Redis
from app.business.portfolio.gateways.cached_portfolio_gateway import CachedPortfolioGateway
from app.business.portfolio.gateways.falcon_portfolio_gateway import FalconPortfolioGateway
from app.cache.portfolio_cache import PortfolioCache
from app.core.config import settings
from app.core.config.redis import get_redis
from app.infrastructure.api_client.rest_client import RestApiClient

# def get_portfolio_gateway() -> FalconPortfolioGateway:
#     return FalconPortfolioGateway(RestApiClient(base_url=settings.MF_API_BASE_URL))

def get_portfolio_gateway(redis: Redis = Depends(get_redis)) -> CachedPortfolioGateway:

    return CachedPortfolioGateway(
        portfolio_gateway=FalconPortfolioGateway(RestApiClient(base_url=settings.MF_API_BASE_URL)),
        portfolio_cache=PortfolioCache(redis)
    )
