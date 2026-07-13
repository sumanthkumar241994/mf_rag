from dataclasses import dataclass

from app.business.goal.models.goal_analysis import GoalAnalysis
from app.workflows.workflow.models.workflow_payload import WorkflowPayload


@dataclass(slots=True)
class GoalWorkflowPayload(WorkflowPayload):
    analysis: GoalAnalysis