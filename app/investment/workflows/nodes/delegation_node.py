from app.investment.base.models import WorkflowError
from app.investment.delegation.delegation_builder_registry import DelegationBuilderRegistry
from app.investment.workflows.investment_state import InvestmentState


class DelegationNode:
    """
    Creates a delegation based on the current workflow state.

    Delegation-specific logic is delegated to the
    DelegationBuilderRegistry.
    """

    def __init__(
        self,
        registry: DelegationBuilderRegistry,
    ) -> None:
        self._registry = registry

    async def __call__(
        self,
        state: InvestmentState,
    ) -> InvestmentState:

        try:
            builder = self._registry.get(state)

        except ValueError as exc:
            state.add_error(
                WorkflowError.from_exception(
                    message=exc,
                    source="delegation",
                )
            )
            return state

        state.delegation = builder.build(state)

        return state