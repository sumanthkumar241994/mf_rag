from fastapi import Depends
from redis.asyncio import Redis
from app.business.customer.gateway.cached_customer_gateway import CachedCustomerGateway
from app.business.customer.gateway.falcon_customer_gateway import FalconCustomerGateway
from app.cache.customer_cache import CustomerCache
from app.core.config import settings
from app.core.config.redis import get_redis
from app.infrastructure.api_client.rest_client import RestApiClient

def get_customer_gateway(redis: Redis=Depends(get_redis)) -> CachedCustomerGateway:
    return CachedCustomerGateway(
        customer_gateway=FalconCustomerGateway(RestApiClient(base_url=settings.MF_API_BASE_URL)),
        customer_cache=CustomerCache(redis)
        )
