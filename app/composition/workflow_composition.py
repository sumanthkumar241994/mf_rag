
from app.business.advisor.enums.capabilities import Capability
from app.workflows.workflow.handlers.base_workflow_handler import BaseWorkflowHandler
from app.workflows.workflow.handlers.goal_workflow_handler import GoalWorkflowHandler
from app.workflows.workflow.registry.workflow_handler_registry import WorkflowHandlerRegistry
from app.workflows.workflow.service.workflow_service import WorkflowService


class WorkflowComposition:

    def __init__(self):
        self.workflow_service = WorkflowService()

    def register(
        self,
        capability: Capability,
        handler: BaseWorkflowHandler,
    ) -> None:
        self.workflow_service.register(
            capability,
            handler,
        )