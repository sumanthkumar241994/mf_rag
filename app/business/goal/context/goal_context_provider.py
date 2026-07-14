from app.business.customer.customer_service import CustomerService
from app.business.portfolio.service.portfolio_service import PortfolioService
from app.workflows.advisor.advisor_state import AdvisorState


class GoalContextProvider:

    def __init__(
        self,
        customer_service: CustomerService,
        portfolio_service: PortfolioService,
    ):
        self._customer_service = customer_service
        self._portfolio_service = portfolio_service

    async def enrich(
        self,
        state: AdvisorState,
    ) -> None:

        if state.customer is None:
            execution = await self._customer_service.retrieve(state)
            if execution:
                state.customer = execution.result

        if state.portfolio_analysis is None:
            execution = await self._portfolio_service.analyze(state)
            if execution:
                state.portfolio_analysis = execution.result