from enum import StrEnum


class Provider(StrEnum):
    ANTHROPIC = "anthropic"
    GEMMA = "gemma"
    TITAN = "titan"
    NOVA = "nova"