from dataclasses import dataclass


@dataclass(slots=True)
class LLMGuardResponse:
    allowed: bool
    confidence: float
    reason: str