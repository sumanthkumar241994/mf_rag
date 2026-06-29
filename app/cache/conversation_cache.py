from __future__ import annotations

import json
from dataclasses import asdict

from uuid import UUID
from redis.asyncio import Redis

from app.schemas.conversation.cache_message import CacheMessage

class ConversationCache:
    """
    Redis cache for recent conversation messages.

    Stores only the last N messages required by the runtime.
    PostgreSQL remains the source of truth.
    """
    DEFAULT_TTL = 60 * 60 * 24
    DEFAULT_MAX_MESSAGES = 20

    def __init__(self, redis: Redis):
        self.redis = redis

    def _key(self, conversation_id: UUID) -> str:
        return f"conversation:{conversation_id}"

    async def exists(self, conversation_id: UUID) -> bool:
        return await self.redis.exists(self._key(conversation_id)) > 0

    async def append_message(self, conversation_id: UUID, message: CacheMessage, max_messages: int = DEFAULT_MAX_MESSAGES):
        key = self._key(conversation_id)
        await self.redis.rpush(key, json.dumps(message.model_dump()))
        await self.redis.ltrim(key, -max_messages, -1)
        await self.redis.expire(key, self.DEFAULT_TTL)

    async def get_messages(self, conversation_id: UUID) -> list[CacheMessage]:
        values = await self.redis.lrange(self._key(conversation_id),0,-1)
        return [ CacheMessage(**json.loads(value)) for value in values]

    async def set_messages(self, conversation_id: UUID, messages: list[CacheMessage]):
        key = self._key(conversation_id)

        pipe = self.redis.pipeline()
        await pipe.delete(key)

        if messages:
            await pipe.rpush(key, *[json.dumps(message.model_dump()) for message in messages])
        await pipe.expire(key, self.DEFAULT_TTL)
        await pipe.execute()
    
    async def delete(self, conversation_id: UUID):
        await self.redis.delete(self._key(conversation_id))
    
    async def refresh_ttl(self, conversation_id: UUID):
        await self.redis.expire(self._key(conversation_id), self.DEFAULT_TTL)

    async def size(self, conversation_id: UUID) -> int:
        return await self.redis.llen(self._key(conversation_id))
    