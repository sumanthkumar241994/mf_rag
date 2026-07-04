from dataclasses import dataclass, field

from app.business.advisor.enums.agent_type import AgentType
from app.business.advisor.enums.intent import Intent
from app.business.advisor.enums.tool_type import ToolType
from app.business.advisor.models.capability_match import CapabilityMatch


@dataclass(slots=True, frozen=True)
class PlannerResult:
    intent: Intent
    capabilities: list[CapabilityMatch] = field(default_factory=list)
    agent: AgentType = AgentType.ADVISOR.value
    selected_tools: list[ToolType] = field(default_factory=list)
    confidence: float = 1.0
    reasoning: str | None = None
