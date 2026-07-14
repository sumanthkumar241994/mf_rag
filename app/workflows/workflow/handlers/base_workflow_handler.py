from abc import ABC, abstractmethod
from typing import Any

from app.workflows.advisor.advisor_state import AdvisorState
from app.workflows.workflow.models.workflow_execution import WorkflowExecution
from app.workflows.workflow.models.workflow_interrupt import WorkflowInterrupt
from app.workflows.workflow.models.workflow_payload import WorkflowPayload
from app.workflows.workflow.models.workflow_resume import WorkflowResume


class BaseWorkflowHandler(ABC):
    @abstractmethod
    def create(self, state: AdvisorState, context: Any) -> WorkflowInterrupt:
        raise NotImplementedError
    
    @abstractmethod
    def resume(self, state: AdvisorState, payload: WorkflowPayload, resume: WorkflowResume) -> WorkflowExecution[Any]:
        raise NotImplementedError