from dataclasses import dataclass, field


@dataclass(slots=True)
class PlannerContext:
    intent: str
    capabilities: list[str] = field(default_factory=list)
    selected_tools: list[str] = field(default_factory=list)
    confidence: float | None = None
    reasoning: str | None = None