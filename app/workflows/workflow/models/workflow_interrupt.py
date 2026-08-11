from dataclasses import dataclass, field
from typing import Any

from app.business.advisor.enums.capabilities import Capability
from app.workflows.workflow.models.workflow_payload import WorkflowPayload


@dataclass(slots=True)
class WorkflowInterrupt:
    capability: Capability
    questions: list[str]
    payload: WorkflowPayload | None = None

    def to_dict(self) -> dict:
        return {
            "capability": self.capability.value,
            "questions": self.questions
        }
    
    def to_message(self) -> str:
        return (
            "Additional information required:\n"
            + "\n".join(
                f"- {question}"
                for question in self.questions
            )
        )