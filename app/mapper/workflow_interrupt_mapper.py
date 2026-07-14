from __future__ import annotations


from app.mapper.goal_workflow_payload_mapper import GoalWorkflowPayloadMapper
from app.workflows.workflow.models.workflow_interrupt import (
    WorkflowInterrupt,
)


class WorkflowInterruptMapper:

    @staticmethod
    def from_dict(
        interrupt: WorkflowInterrupt | dict,
    ) -> WorkflowInterrupt:

        if isinstance(
            interrupt,
            WorkflowInterrupt,
        ):
            return interrupt

        payload = interrupt.get("payload")

        if payload is not None:
            payload = GoalWorkflowPayloadMapper.from_dict(
                payload,
            )

        return WorkflowInterrupt(
            capability=interrupt["capability"],
            questions=interrupt["questions"],
            payload=payload,
        )