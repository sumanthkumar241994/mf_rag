from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict

from app.investment.workflows.models.workflow_interrupt import WorkflowInterrupt


T = TypeVar("T")


class WorkflowExecution(BaseModel, Generic[T]):
    model_config = ConfigDict(arbitrary_types_allowed=True)

    result: T
    interrupt: WorkflowInterrupt | None = None

    @property
    def interrupted(self) -> bool:
        return self.interrupt is not None