from __future__ import annotations

from app.business.goal.mapper.goal_mapper import GoalMapper
from app.workflows.workflow.models.goal_workflow_payload import (
    GoalWorkflowPayload,
)


class GoalWorkflowPayloadMapper:

    @staticmethod
    def from_dict(
        payload: GoalWorkflowPayload | dict,
    ) -> GoalWorkflowPayload:

        if isinstance(payload, GoalWorkflowPayload):
            return payload

        return GoalWorkflowPayload(
            analysis=GoalMapper.from_dict(
                payload["analysis"],
            ),
        )