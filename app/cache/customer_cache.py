from __future__ import annotations

import json
from typing import Any

from redis.asyncio import Redis


class CustomerCache:
    """
    Redis cache for customer profile.

    Falcon remains the source of truth.
    """

    DEFAULT_TTL = 60 * 60 * 24  # 24 hours

    def __init__(self, redis: Redis):
        self.redis = redis

    def _key(self, customer_id: str) -> str:
        return f"customer:{customer_id}"

    async def exists(
        self,
        customer_id: str,
    ) -> bool:
        return await self.redis.exists(
            self._key(customer_id)
        ) > 0

    async def get(
        self,
        customer_id: str,
    ) -> dict[str, Any] | None:

        value = await self.redis.get(
            self._key(customer_id)
        )

        if value is None:
            return None

        return json.loads(value)

    async def set(
        self,
        customer_id: str,
        customer: dict[str, Any],
    ) -> None:

        await self.redis.set(
            self._key(customer_id),
            json.dumps(customer),
            ex=self.DEFAULT_TTL,
        )

    async def delete(
        self,
        customer_id: str,
    ) -> None:

        await self.redis.delete(
            self._key(customer_id)
        )

    async def refresh_ttl(
        self,
        customer_id: str,
    ) -> None:

        await self.redis.expire(
            self._key(customer_id),
            self.DEFAULT_TTL,
        )