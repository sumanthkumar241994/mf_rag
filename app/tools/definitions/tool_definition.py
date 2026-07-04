from dataclasses import dataclass, field

from app.business.advisor.enums.agent_type import AgentType
from app.business.advisor.enums.capabilities import Capability

@dataclass(slots=True, frozen=True)
class ToolDefinition:
    name: str
    description: str
    capability: Capability
    timeout_seconds: int = 30
    enabled: bool = True
    allowed_agents: list[AgentType] = field(default_factory=list)
    version: str = '1.0'
    tags: list[str] = field(default_factory=list)