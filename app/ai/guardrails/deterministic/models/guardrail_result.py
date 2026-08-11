from dataclasses import dataclass

from app.ai.guardrails.enums import GuardRailCategory

@dataclass(slots=True)
class GuardRailResult:
    allowed: bool
    category: GuardRailCategory | None = None
    reason: str | None = None
    response: str | None = None
    validator: str | None = None