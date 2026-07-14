from dataclasses import dataclass, field
from typing import Any

from app.business.advisor.enums.capabilities import Capability
from app.workflows.workflow.models.workflow_payload import WorkflowPayload


@dataclass(slots=True)
class WorkflowInterrupt:
    capability: Capability
    questions: list[str]
    payload: WorkflowPayload | None = None
    