from app.investment.business.customer.models.fatca import Fatca
from app.investment.business.customer.models.nominee import Nominee
from app.investment.business.execution.goal.execution_goal import ExecutionGoal
from app.investment.common.enums.operation_type import OperationType

class UpdateFatcaExecutionGoal(ExecutionGoal):
    operation: OperationType = OperationType.UPDATE_FATCA
    customer_id: str
    fatca: Fatca | None = None