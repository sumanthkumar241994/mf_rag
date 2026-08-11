from pydantic import BaseModel

from app.investment.common.enums.operation_type import OperationType



class ExecutionGoal(BaseModel):
    operation: OperationType