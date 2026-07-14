from app.business.advisor.enums.capabilities import Capability
from app.workflows.workflow.handlers.base_workflow_handler import BaseWorkflowHandler


class WorkflowHandlerRegistry:
    def __init__(self):
        self._handlers = {}

    def register(self, capability: Capability, handler: BaseWorkflowHandler):
        self._handlers[capability] = handler

    def get(self, capability: Capability) -> BaseWorkflowHandler:
        return self._handlers[capability]