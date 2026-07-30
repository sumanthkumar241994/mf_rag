from __future__ import annotations

from typing import Generic, TypeVar

from app.business.advisor.enums.capabilities import Capability
from app.workflows.workflow.models.workflow_execution import WorkflowExecution
from app.workflows.workflow.service.workflow_service import WorkflowService

T = TypeVar("T")


class BaseWorkflowService(Generic[T]):
    """
    Base class for workflow services.

    Responsible for creating WorkflowExecution instances and
    delegating interrupt creation to WorkflowService.
    """

    def __init__(
        self,
        workflow_service: WorkflowService,
    ):
        self._workflow_service = workflow_service

    def create_workflow_execution(
        self,
        *,
        capability: Capability,
        result: T,
        completed: bool,
        context: object | None = None,
    ) -> WorkflowExecution[T]:
        """
        Creates a WorkflowExecution.

        If the workflow is not completed, an interrupt is created
        so execution can later resume.
        """

        interrupt = None

        if not completed:
            interrupt = self._workflow_service.create(
                capability=capability,
                context=context or result,
            )

        return WorkflowExecution(
            result=result,
            interrupt=interrupt,
        )