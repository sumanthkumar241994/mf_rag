

from app.investment.business.execution.action_registry import ActionHandlerRegistry
from app.investment.models.action_type import NextAction
from app.investment.workflows.investment_state import InvestmentState


class ActionDispatcher:

    def __init__(
        self,
        registry: ActionHandlerRegistry,
    ):
        self._registry = registry

    async def execute(
        self,
        state: InvestmentState,
        action: NextAction,
    ) -> None:

        handler = self._registry.get(action.action)

        await handler.execute(
            state=state,
            action=action,
        )