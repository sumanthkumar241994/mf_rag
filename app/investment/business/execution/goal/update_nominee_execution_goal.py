from app.investment.business.customer.models.nominee import Nominee
from app.investment.business.execution.goal.execution_goal import ExecutionGoal
from app.investment.common.enums.operation_type import OperationType


class UpdateNomineeExecutionGoal(ExecutionGoal):
    operation: OperationType = OperationType.UPDATE_NOMINEE
    customer_id: str
    nominee: Nominee | None = None