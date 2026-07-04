from dataclasses import dataclass, field

from app.business.advisor.enums.capabilities import Capability
from app.business.advisor.enums.intent import Intent


@dataclass(slots=True)
class CapabilityRule:
    capability: Capability
    # Primary business keywords
    keywords: list[str]
    # Alternative phrases
    synonyms: list[str] = field(default_factory=list)
    # Example user utterances
    examples: list[str] = field(default_factory=list)
    # Confidence contribution
    weight: float = 1.0
    # Evaluation order (lower evaluated first)
    priority: int = 100
    supported_intents: set[Intent] | None = None