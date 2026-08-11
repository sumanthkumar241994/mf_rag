from dataclasses import dataclass, field

from app.business.advisor.enums.capabilities import Capability
from app.business.advisor.enums.intent import Intent
from app.business.advisor.models.capability_match import CapabilityMatch
from app.business.advisor.planner.models.planner_reason import PlannerReason


@dataclass
class PlannerResponse:
    intent: Intent
    confidence: float
    
    reasoning: str | None = None
    reasons: list[PlannerReason] = field(default_factory=list)

    @property
    def capabilities(self) -> list[Capability]:
        return [reason.capability for reason in self.reasons]

    @property
    def capability_matches(self) -> list[CapabilityMatch]:
        return [ CapabilityMatch(reason.capability) for reason in self.reasons ]