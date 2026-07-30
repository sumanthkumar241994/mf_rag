from __future__ import annotations

from app.investment.base.models import InvestmentBaseModel, WorkflowError
from app.investment.business.customer.models.customer import Customer
from pydantic import BaseModel, ConfigDict, Field
from app.dtos.request_context import RequestContext

from app.workflows.workflow.models.workflow_execution import WorkflowExecution
from app.workflows.workflow.models.workflow_interrupt import WorkflowInterrupt


class InvestmentState(InvestmentBaseModel):
    """
    Shared state for the Investment Agent workflow.
    """

    # ------------------------------------------------------------------
    # Request Context
    # ------------------------------------------------------------------

    request: RequestContext

    trace_id: str
    correlation_id: str | None = None

    # ------------------------------------------------------------------
    # Workflow
    # ------------------------------------------------------------------

    workflow_execution: WorkflowExecution | None = None
    workflow_interrupt: WorkflowInterrupt | None = None

    # ------------------------------------------------------------------
    # Customer
    # ------------------------------------------------------------------

    customer: Customer | None = None

    # ------------------------------------------------------------------
    # Execution Context
    # ------------------------------------------------------------------

    metadata: dict[str, object] = Field(default_factory=dict)

    # ------------------------------------------------------------------
    # Errors
    # ------------------------------------------------------------------

    errors: list[WorkflowError] = Field(default_factory=list)

    def add_error(self, error: WorkflowError) -> None:
        self.errors.append(error)
    
    def get_latest_error(self, source: str) -> WorkflowError | None:
        for error in reversed(self.errors):
            if error.source == source:
                return error
            
        return None
    
    def clear_error(self, source: str):
        self.errors = [error for error in self.errors if error.source != source]