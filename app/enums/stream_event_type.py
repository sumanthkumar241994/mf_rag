from enum import StrEnum

class StreamEventType(StrEnum):
    SESSION = "session"
    TOKEN = "token"
    COMPLETED = "completed"
    ERROR = "error"
    
    PLANNER_START ='planner_start'
    PLANNER_END = 'planner_end'

    TOOL_START = "tool_start"
    TOOL_END = "tool_end"

    PROMPT_START = 'prompt_start'
    PROMPT_END = 'prompt_end'




