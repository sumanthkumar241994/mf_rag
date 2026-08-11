from pydantic import BaseModel

from app.investment.business.execution.goal.execution_goal import ExecutionGoal


class ExecutionWorkflow(BaseModel):
    goals: list[ExecutionGoal]
    current_goal_index: int = 0