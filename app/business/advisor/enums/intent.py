from enum import StrEnum


class Intent(StrEnum):
    """
    Represents the primary objective of the user's request.

    The Planner identifies a single primary intent,
    while one or more capabilities determine which
    business domains are required.
    """
    # Conversation
    GREETING = "greeting"
    CHITCHAT = "chitchat"
    HELP = "help"

    # Read / Understand
    INFORMATION = "information"
    ANALYSIS = "analysis"
    COMPARISON = "comparison"

    # Advise / Plan
    RECOMMENDATION = "recommendation"
    PLANNING = "planning"

    # Perform an action
    EXECUTION = "execution"

    # Unknown
    UNKNOWN = "unknown"