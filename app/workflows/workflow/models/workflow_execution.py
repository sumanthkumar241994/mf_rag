from typing import Generic, TypeVar
from dataclasses import dataclass

from app.workflows.workflow.models.workflow_interrupt import WorkflowInterrupt

T =TypeVar("T")

@dataclass(slots=True)
class WorkflowExecution(Generic[T]):
    result: T
    interrupt: WorkflowInterrupt | None = None

    @property
    def interrupted(self) -> bool:
        return self.interrupt is not None
    