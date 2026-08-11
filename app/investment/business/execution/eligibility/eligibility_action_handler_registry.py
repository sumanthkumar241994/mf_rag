from app.investment.business.execution.action_handler import ActionHandler
from app.investment.business.execution.action_registry import ActionHandlerRegistry
from app.investment.business.execution.complete_action_handler import CompletionActionHandler
from app.investment.business.execution.eligibility.handlers.data_collection_interrupt_handler import DataCollectionInterruptHandler
from app.investment.business.execution.eligibility.handlers.eligibility_action_handler import EligibilityActionHandler
from app.investment.common.enums.action_type import ActionType


class EligibilityActionHandlerRegistry(ActionHandlerRegistry):

    def __init__(
        self,
        eligibility_action_handler: EligibilityActionHandler,
        data_collection_interrupt_handler: DataCollectionInterruptHandler,
    ):
        self._handlers: dict[ActionType, ActionHandler] = {
            ActionType.REQUEST_DATA_COLLECTION: data_collection_interrupt_handler,
            ActionType.CHECK_ELIGIBILITY: eligibility_action_handler,
        }

    def get(
        self,
        action: ActionType,
    ) -> ActionHandler:
        return self._handlers[action]