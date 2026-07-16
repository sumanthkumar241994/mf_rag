from enum import StrEnum


class ModelProfile(StrEnum):
    CHAT = "chat"
    PLANNER = "planner"
    TITLE = "title"
    SUMMARY = "summary"
    MEMORY = "memory"
    REFLECTION = "reflection"
    EVALUATION = "evaluation"
    EMBEDDING = "embedding"