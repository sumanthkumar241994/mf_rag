from dataclasses import dataclass
from typing import Any

from app.business.advisor.enums.agent_type import AgentType
from app.enums.workflow import WorkflowType


@dataclass(slots=True)
class AgentPlan:
    primary_agent: AgentType
    workflow: WorkflowType | None = None
    confidence: float = 1.0
    reason: str | None = None
    metadata: dict[str, Any] | None = None

    def to_dict(self) -> dict[str, Any]:
        workflow = self.workflow.value if self.workflow else None
        return {
            "agent": self.primary_agent.value,
            "workflow": workflow,
            "confidence": self.confidence,
            "reason": self.reason,
            "metadata": self.metadata,
        }