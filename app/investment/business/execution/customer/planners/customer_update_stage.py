from app.investment.business.execution.planner_stage import PlannerStage
from app.investment.common.enums.operation_type import OperationType
from app.investment.models.action_type import NextAction
from app.investment.common.enums.action_type import ActionType
from app.investment.workflows.investment_state import InvestmentState

class OperationActionMapper:

    _MAP = {
        OperationType.UPDATE_NOMINEE: ActionType.UPDATE_NOMINEE,
        OperationType.UPDATE_FATCA: ActionType.UPDATE_FATCA,
        # add other operations here
    }

    @classmethod
    def map(
        cls,
        operation: OperationType,
    ) -> ActionType:

        try:
            return cls._MAP[operation]
        except KeyError as exc:
            raise ValueError(
                f"No ActionType mapping exists for "
                f"operation: {operation}"
            ) from exc

class CustomerActionStage(PlannerStage):

    async def plan(
        self,
        state: InvestmentState,
    ) -> NextAction | None:
        
        # Resume pending customer action.
        if state.execution_goal is not None:
            action = OperationActionMapper.map(
                state.execution_goal.operation,
            )
            return NextAction(
                action=action,
                payload=state.execution_goal.model_dump(mode='json'),
            )

        return None