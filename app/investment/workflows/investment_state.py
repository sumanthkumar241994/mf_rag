from __future__ import annotations

from app.investment.base.models import InvestmentBaseModel, WorkflowError
from app.investment.business.customer.models.customer import Customer
from pydantic import BaseModel, ConfigDict, Field
from app.dtos.request_context import RequestContext

from app.investment.business.execution.goal.execution_goal import ExecutionGoal
from app.investment.business.otp.models.verification_state import VerificationState
from app.investment.common.enums.customer_state import CustomerState
from app.investment.models.action_type import NextAction
from app.investment.models.eligibility import Eligibility
from app.investment.workflows.models.delegation import Delegation
from app.investment.workflows.models.workflow_execution import WorkflowExecution
from app.investment.workflows.models.workflow_interrupt import WorkflowInterrupt
from app.investment.workflows.models.workflow_resume import WorkflowResume


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

    delegation: Delegation | None = None

    execution_goal: ExecutionGoal | None = None
    eligibility: Eligibility | None = None

    next_action: NextAction | None = None

    pending_actions: list[NextAction] = Field(default_factory=list)
    pending_action: NextAction | None = None

    verification: VerificationState | None = None
    # ------------------------------------------------------------------
    # Workflow
    # ------------------------------------------------------------------

    workflow_execution: WorkflowExecution | None = None
    workflow_interrupt: WorkflowInterrupt| None = None
    workflow_resume: WorkflowResume | None = None

    # ------------------------------------------------------------------
    # Customer
    # ------------------------------------------------------------------

    customer: Customer | None = None
    customer_state: CustomerState = CustomerState.NOT_LOADED

    # ------------------------------------------------------------------
    # Execution Context
    # ------------------------------------------------------------------

    metadata: dict[str, object] = Field(default_factory=dict)

    # ------------------------------------------------------------------
    # Errors
    # ------------------------------------------------------------------

    errors: list[WorkflowError] = Field(default_factory=list)
    last_error: WorkflowError | None = None

    def add_error(self, error: WorkflowError) -> None:
        self.last_error = error
        self.errors.append(error)
    
    def get_latest_error(self, source: str) -> WorkflowError | None:
        for error in reversed(self.errors):
            if error.source == source:
                return error
            
        return None
    
    def clear_error(self, source: str):
        self.errors = [error for error in self.errors if error.source != source]