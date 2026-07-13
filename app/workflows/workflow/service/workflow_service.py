from typing import Any
from app.business.advisor.enums.capabilities import Capability
from app.workflows.advisor.advisor_state import AdvisorState
from app.workflows.workflow.handlers.base_workflow_handler import BaseWorkflowHandler
from app.workflows.workflow.models.workflow_execution import WorkflowExecution
from app.workflows.workflow.models.workflow_interrupt import WorkflowInterrupt
from app.workflows.workflow.models.workflow_payload import WorkflowPayload
from app.workflows.workflow.models.workflow_resume import WorkflowResume
from app.workflows.workflow.registry.workflow_handler_registry import WorkflowHandlerRegistry


class WorkflowService:
    def __init__(self):
        self._registry = WorkflowHandlerRegistry()

    def register(self, capability: Capability, handler: BaseWorkflowHandler):
        self._registry.register(capability, handler)
    
    def create(self, state: AdvisorState, capability: Capability, context: Any) -> WorkflowInterrupt:
        handler = self._registry.get(capability)
        return handler.create(state=state, context=context)

    async def resume(self, state: AdvisorState, capability: Capability, payload: WorkflowPayload, resume: WorkflowResume) -> WorkflowExecution[Any]:
        handler = self._registry.get(capability)

        return await handler.resume(
            state=state,
            payload=payload,
            resume=resume
        )