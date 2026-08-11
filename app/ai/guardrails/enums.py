from enum import StrEnum


class GuardRailCategory(StrEnum):
    INPUT_SIZE = "input_size"
    PROMPT_INJECTION = "prompt_injection"
    ABUSE = "abuse"
    DOMAIN = "domain"
    RATE_LIMIT = "rate_limit"
    UNKNOWN = "unknown"