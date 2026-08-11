from enum import StrEnum


class RoutingStrategy(StrEnum):
    RULE_BASED = "rule_based"
    LLM = "llm"
    HYBRID = "hybrid"