from app.investment.base.models import InvestmentBaseModel, RequestContext
from app.investment.business.execution.goal.update_fatca_execution_goal import UpdateFatcaExecutionGoal


class UpdateFatcaRequest(InvestmentBaseModel):
    trace_id: str
    request: RequestContext
    goal: UpdateFatcaExecutionGoal