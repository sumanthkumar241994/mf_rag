from enum import StrEnum

class StreamEventType(StrEnum):
    MESSAGE_SAVED = 'message_saved'
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

    WORKFLOW_INTERRUPT = 'workflow_interrupt'
    WORKFLOW_COMPLETED = 'workflow_completed'

    WORKFLOW_DELEGATION = 'workflow_delegation'



