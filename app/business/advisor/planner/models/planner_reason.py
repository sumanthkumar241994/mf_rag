from dataclasses import dataclass

from app.business.advisor.enums.capabilities import Capability


@dataclass
class PlannerReason:
    capability: Capability
    reason: str