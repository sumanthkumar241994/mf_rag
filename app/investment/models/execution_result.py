from enum import StrEnum

from pydantic import BaseModel

from app.investment.workflows.models.workflow_execution import WorkflowExecution



class ExecutionStatus(StrEnum):
    COMPLETED = "completed"
    CONTINUE = "continue"
    INTERRUPTED = "interrupted"
    FAILED = "failed"


class ExecutionResult(BaseModel):
    status: ExecutionStatus
    execution: WorkflowExecution | None = None