from dataclasses import dataclass

from app.business.advisor.enums.capabilities import Capability


@dataclass(slots=True, frozen=True)
class CapabilityMatch:
    capability: Capability
    confidence: float | None = None
    matched_phrase: str | None = None
    rule_priority: int | None = None
