from datetime import date
from decimal import Decimal
from app.investment.business.execution.goal.execution_goal import ExecutionGoal
from app.investment.business.investment.enums.product_type import InvestmentProduct
from app.investment.business.investment.models.scheme_allocation import SchemeAllocation
from app.investment.business.investment.models.sip_details import SipDetails
from app.investment.common.enums.operation_type import OperationType


class InvestmentExecutionGoal(ExecutionGoal):
    operation: OperationType = OperationType.INVEST
    product: InvestmentProduct
    amount: Decimal
    portfolio: list[SchemeAllocation]
    sip: SipDetails | None = None
    source: str = "search"
    target_completion_on: date | None = None