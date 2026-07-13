from __future__ import annotations

from app.business.goal.mapper.goal_mapper import GoalMapper

from app.mapper.workflow_interrupt_mapper import WorkflowInterruptMapper
from app.workflows.workflow.models.workflow_execution import (
    WorkflowExecution,
)


class WorkflowExecutionMapper:

    @staticmethod
    def from_dict(
        execution: WorkflowExecution | dict,
    ) -> WorkflowExecution:

        if isinstance(
            execution,
            WorkflowExecution,
        ):
            return execution

        result = execution.get("result")

        if result is not None:
            result = GoalMapper.from_dict(result)

        interrupt = execution.get("interrupt")

        if interrupt is not None:
            interrupt = WorkflowInterruptMapper.from_dict(
                interrupt,
            )

        return WorkflowExecution(
            result=result,
            interrupt=interrupt,
        )