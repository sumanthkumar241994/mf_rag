from app.investment.business.execution.action_handler import ActionHandler
from app.investment.workflows.investment_state import InvestmentState
from app.workflows.workflow.models.workflow_execution import WorkflowExecution


class CompletionActionHandler(ActionHandler):

    async def execute(
        self,
        state: InvestmentState,
    ) -> None:

        execution = state.workflow_execution or WorkflowExecution()

        execution.completed = True

        if execution.result is None:
            execution.result = state.result

        state.workflow_execution = execution