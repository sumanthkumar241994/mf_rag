from typing import Any
from app.investment.business.customer.models.customer import Customer
from app.investment.business.customer.models.nominee import Nominee
from app.investment.business.execution.goal.execution_goal import ExecutionGoal
from app.investment.business.otp.enums.verification_purpose import VerificationPurpose
from app.investment.common.enums.operation_type import OperationType


class UpdateNomineeExecutionGoal(ExecutionGoal):
    operation: OperationType = OperationType.UPDATE_NOMINEE
    customer_id: str
    nominee: Nominee | None = None
    verification_purpose : VerificationPurpose = VerificationPurpose.CUSTOMER_UPDATE

    @property
    def requires_verification(self) -> bool:
        return True
    
    def verification_payload(
        self,
        customer: Customer,
    ) -> dict[str, Any]:

        return {
            "customer_action_params": {
                "transaction_type": "NOMINEE",
                "nominee_opt": "Y",
            },
            "mobile": customer.profile.mobile,
        }