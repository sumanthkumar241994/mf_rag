from enum import StrEnum


class WorkflowDecision(StrEnum):
    CONTINUE = 'continue'
    TOOL_FAILURE = 'tool_failure'