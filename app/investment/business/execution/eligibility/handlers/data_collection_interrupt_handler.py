from app.investment.business.execution.action_handler import ActionHandler
from app.investment.business.execution.eligibility_action_mapper import EligibilityActionMapper
from app.investment.models.action_type import NextAction
from app.investment.models.eligibility_requirement import EligibilityRequirement
from app.investment.models.execution_result import ExecutionResult, ExecutionStatus
from app.investment.workflows.investment_state import InvestmentState
from app.investment.common.enums.interrupt_type import InterruptType
from app.investment.workflows.models.workflow_execution import WorkflowExecution
from app.investment.workflows.models.workflow_interrupt import WorkflowInterrupt


class DataCollectionInterruptHandler(ActionHandler):

    def __init__(self, eligibility_action_mapper: EligibilityActionMapper):
        self._eligibility_action_mapper = eligibility_action_mapper

    async def execute(
        self,
        state: InvestmentState,
        action: NextAction,
    ) -> ExecutionResult:

        eligibility = state.eligibility

        if eligibility is None:
            raise ValueError(
                "Eligibility is not available."
            )
        
        state.pending_actions = [
            self._eligibility_action_mapper.map(requirement)
            for requirement in eligibility.required
        ]

        workflow_execution = workflow_execution = WorkflowExecution(
            result=eligibility,
            interrupt=WorkflowInterrupt(
                type=InterruptType.COLLECT_DATA,
                title="Additional information required",
                message=(
                    "Please complete the following steps before continuing."
                ),
                data=eligibility.required,
            ),
        )

        state.workflow_execution = workflow_execution

        return ExecutionResult(status=ExecutionStatus.COMPLETED, execution=workflow_execution)