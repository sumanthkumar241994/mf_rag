from dataclasses import dataclass, field

@dataclass(slots=True)
class ToolDefinition:
    name: str
    description: str
    category: str
    timeout_seconds: int = 30
    enabled: bool = True
    allowed_agents: list[str] = field(default_factory=list)
    version: str = '1.0'
    tags: list[str] = field(default_factory=list)