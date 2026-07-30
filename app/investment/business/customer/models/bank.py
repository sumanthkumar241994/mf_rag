from decimal import Decimal

from pydantic import computed_field

from app.investment.base.models import InvestmentBaseModel


class Bank(InvestmentBaseModel):
    bank_name: str | None = None
    verified: bool = False
    validated: bool = False
    updated: bool = False
    mandate_status: str | None = None
    mandate_limit: Decimal | None = None
    auto_debit_enabled: bool = False

    @computed_field
    @property
    def description(self) -> str:
        if self.validated:
            return "Your bank account has been successfully verified."

        if self.updated:
            return (
                "Your bank account has been added and is pending verification."
            )

        return "No bank account has been added."