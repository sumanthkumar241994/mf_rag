from app.investment.base.models import InvestmentBaseModel, RequestContext
from app.investment.business.execution.goal.update_nominee_execution_goal import UpdateNomineeExecutionGoal


class UpdateNomineeRequest(InvestmentBaseModel):
    trace_id: str
    request: RequestContext
    goal: UpdateNomineeExecutionGoal
    verification_id: str