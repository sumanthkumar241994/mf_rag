from enum import Enum

class QueuePriority(str, Enum):
    HIGH = "high"
    MEDIUM = 'medium'
    LOW = 'low'