from dataclasses import dataclass


@dataclass(slots=True)
class GuardRailResult:
    allowed: bool
    reason: str | None = None
    response: str | None = None