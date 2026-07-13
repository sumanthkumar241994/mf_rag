from app.business.advisor.enums.capabilities import Capability
from app.business.goal.models.goal_analysis import GoalAnalysis
from app.business.goal.service.goal_service import GoalService
from app.workflows.advisor.advisor_state import AdvisorState
from app.workflows.workflow.handlers.base_workflow_handler import BaseWorkflowHandler
from app.workflows.workflow.models.goal_workflow_payload import GoalWorkflowPayload
from app.workflows.workflow.models.workflow_execution import WorkflowExecution
from app.workflows.workflow.models.workflow_interrupt import WorkflowInterrupt
from app.workflows.workflow.models.workflow_payload import WorkflowPayload
from app.workflows.workflow.models.workflow_resume import WorkflowResume


class GoalWorkflowHandler(BaseWorkflowHandler):

    def __init__(
        self,
        goal_service: GoalService
    ):
        self._goal_service = goal_service

    def create(self, state: AdvisorState, context: GoalAnalysis) -> WorkflowInterrupt:
        return WorkflowInterrupt(
            capability=Capability.GOAL,
            questions=context.parameter_resolution.follow_up_questions,
            payload=GoalWorkflowPayload(
                analysis=context
            )
        )
    
    async def resume(self, state: AdvisorState, payload: GoalWorkflowPayload, resume: WorkflowResume) -> WorkflowExecution[GoalAnalysis]:
        return await self._goal_service.resume(
            state=state,
            payload=payload,
            resume=resume
        )