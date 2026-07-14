from typing import Generic, TypeVar

from app.business.advisor.enums.capabilities import Capability
from app.workflows.advisor.advisor_state import AdvisorState
from app.workflows.workflow.models.workflow_execution import WorkflowExecution
from app.workflows.workflow.service.workflow_service import WorkflowService


T = TypeVar("T")


class BaseWorkflowService(Generic[T]):

    def __init__(
        self,
        workflow_service: WorkflowService,
    ):
        self._workflow_service = workflow_service

    def _create_workflow_execution(
        self,
        state: AdvisorState,
        capability: Capability,
        result: T,
        complete: bool,
    ) -> WorkflowExecution[T]:

        interrupt = None

        if not complete:
            interrupt = self._workflow_service.create(
                state=state,
                capability=capability,
                context=result,
            )

        return WorkflowExecution(
            result=result,
            interrupt=interrupt,
        )