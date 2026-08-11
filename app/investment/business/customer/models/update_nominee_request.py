from app.dtos.request_context import RequestContext
from app.investment.base.models import InvestmentBaseModel
from app.investment.business.execution.goal.update_nominee_execution_goal import UpdateNomineeExecutionGoal


class UpdateNomineeRequest(InvestmentBaseModel):
    trace_id: str
    request: RequestContext
    goal: UpdateNomineeExecutionGoal