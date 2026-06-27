from enum import Enum

class WorkflowType(str, Enum):
    ADVISOR = "advisor"
    COMPARISION = "comparision"
    PLANNING = 'planning'
    PORTFOLIO = 'portfolio'