from app.investment.business.execution.action_handler import ActionHandler
from app.investment.models.action_type import NextAction
from app.investment.models.eligibility_requirement import EligibilityRequirement
from app.investment.workflows.investment_state import InvestmentState
from app.investment.common.enums.interrupt_type import InterruptType
from app.investment.workflows.models.workflow_execution import WorkflowExecution
from app.investment.workflows.models.workflow_interrupt import WorkflowInterrupt


class DataCollectionInterruptHandler(ActionHandler):

    async def execute(
        self,
        state: InvestmentState,
        action: NextAction,
    ) -> None:

        eligibility = state.eligibility

        if eligibility is None:
            raise ValueError(
                "Eligibility is not available."
            )

        state.workflow_execution = WorkflowExecution(
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