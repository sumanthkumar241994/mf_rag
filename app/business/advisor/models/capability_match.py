from dataclasses import dataclass

from app.business.advisor.enums.capabilities import Capability


@dataclass(slots=True, frozen=True)
class CapabilityMatch:
    capability: Capability
    confidence: float
    matched_phrase: str
    rule_priority: int
