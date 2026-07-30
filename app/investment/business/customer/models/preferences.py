from app.investment.base.models import InvestmentBaseModel


class CustomerPreferences(InvestmentBaseModel):
    push_notifications_enabled: bool = False
    newsletter_enabled: bool = False
    summary_day: str | None = None
    reminder_days: int | None = None
    payment_preference: str | None = None