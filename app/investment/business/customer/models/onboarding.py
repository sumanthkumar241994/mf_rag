from app.investment.base.models import InvestmentBaseModel


class Onboarding(InvestmentBaseModel):
    status: str | None = None
    error: str | None = None