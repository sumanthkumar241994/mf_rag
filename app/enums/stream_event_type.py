from enum import StrEnum

class StreamEventType(StrEnum):
    TOKEN = "token"
    COMPLETED = "completed"
    TOOL_START = "tool_start"
    TOOL_END = "tool_end"
    ERROR = "error"


