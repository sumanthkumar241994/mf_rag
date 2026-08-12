from app.investment.business.execution.action_handler import ActionHandler
from app.investment.common.enums.interrupt_type import InterruptType
from app.investment.models.eligibility_summary import EligibilitySummary
from app.investment.models.execution_result import ExecutionResult, ExecutionStatus
from app.investment.workflows.investment_state import (
    InvestmentState,
)
from app.investment.workflows.models.workflow_execution import WorkflowExecution
from app.investment.workflows.models.workflow_interrupt import WorkflowInterrupt


class EligibilityActionHandler(ActionHandler):

    async def execute(
        self,
        state: InvestmentState,
    ) -> ExecutionResult:

        eligibility = state.eligibility

        summary = EligibilitySummary(
            required=eligibility.required,
            pending=eligibility.pending,
        )

        workflow_execution = workflow_execution = WorkflowExecution(
            result=None,
            interrupt=WorkflowInterrupt[EligibilitySummary] (
                type=InterruptType.ELIGIBILITY,
                title="Complete Investment Prerequisites",
                message=(
                    "Before I can proceed with your investment, "
                    "please complete the required steps."
                ),
                data=summary,
            ),
        )

        state.workflow_execution = workflow_execution

        return ExecutionResult(status=ExecutionStatus.CONTINUE, execution=workflow_execution)