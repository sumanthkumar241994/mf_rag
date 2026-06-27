from dataclasses import dataclass, field
from typing import Any
from app.schemas.conversation.cache_message import CacheMessage

@dataclass(slots=True)
class AgentRequest:
    query: str
    conversation: list[CacheMessage]
    metadata: dict[str, Any] = field(default_factory=dict)