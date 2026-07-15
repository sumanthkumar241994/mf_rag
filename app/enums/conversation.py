from enum import Enum, StrEnum

class ConversationStatus(str, Enum):
    ACTIVE = 'ACTIVE'
    COMPLETED = 'COMPLETED'
    FAILED = 'FAILED'
    ABANDONED = 'ABANDONED'
    ARCHIVED = 'ARCHIVED'

class MessageRole(str, Enum):
    USER = "user"
    ASSISTANT = "assistant"
    SYSTEM = "system"

class MessageType(StrEnum):
    TEXT = "text"
    TOOL = "tool"
    INTERRUPT = "interrupt"
    RESUME = "resume"
    SUMMARY = "summary"
    TITLE = "title"
    EVENT = "event"