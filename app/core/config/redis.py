from redis.asyncio import Redis

from app.core.config.settings import settings

redis_client = Redis.from_url(settings.REDIS_URL, decode_responses=True)


def get_redis() -> Redis:
    return redis_client