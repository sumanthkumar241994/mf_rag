from app.investment.business.execution.action_handler import ActionHandler
from app.investment.business.execution.complete_action_handler import CompletionActionHandler
from app.investment.business.execution.customer.handlers.customer_action_handler import CustomerActionHandler
from app.investment.business.execution.customer.handlers.fatca_update_action_handler import FatcaUpdateActionHandler
from app.investment.business.execution.customer.handlers.nominee_update_action_handler import NomineeUpdateActionHandler
from app.investment.common.enums.action_type import ActionType


class CustomerActionHandlerRegistry:

    def __init__(
        self,
        customer_action_handler: CustomerActionHandler,
        nominee_action_handler: NomineeUpdateActionHandler,
        fatca_action_handler: FatcaUpdateActionHandler
    ):
        self._handlers: dict[
            ActionType,
            ActionHandler,
        ] = {
            ActionType.CHECK_CUSTOMER: customer_action_handler,
            ActionType.UPDATE_NOMINEE: nominee_action_handler,
            ActionType.UPDATE_FATCA: fatca_action_handler
        }

    def get(
        self,
        action: ActionType,
    ) -> ActionHandler:
        return self._handlers[action]