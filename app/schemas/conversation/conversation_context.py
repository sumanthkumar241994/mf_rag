from pydantic import BaseModel
from app.models.conversation import Conversation
from app.schemas.conversation.cache_message import CacheMessage

class ConversationContext(BaseModel):
    conversation: Conversation
    messages: list[CacheMessage]
    