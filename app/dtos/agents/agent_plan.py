from dataclasses import dataclass
from typing import Any

from app.business.advisor.enums.agent_type import AgentType


@dataclass(slots=True)
class AgentPlan:
    agents: list[AgentType]
    reason: str | None = None
    metadata: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "agents": [agent.value for agent in self.agents],
            "reason": self.reason,
            "metadata": self.metadata,
        }