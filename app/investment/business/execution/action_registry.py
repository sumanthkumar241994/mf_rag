

from app.investment.business.execution.action_handler import ActionHandler
from app.investment.common.enums.action_type import ActionType


class ActionHandlerRegistry:

    def __init__(
        self,
        handlers: dict[ActionType, ActionHandler],
    ):
        self._handlers = handlers

    def get(
        self,
        action: ActionType,
    ) -> ActionHandler:

        try:
            return self._handlers[action]

        except KeyError:
            raise ValueError(
                f"No handler registered for action '{action.value}'"
            )