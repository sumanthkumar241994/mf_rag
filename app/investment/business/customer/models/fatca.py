from app.investment.base.models import InvestmentBaseModel
from app.investment.business.customer.enums.address_type import AddressType
from app.investment.business.customer.enums.annual_income_code import AnnualIncomeCode
from app.investment.business.customer.enums.fatca_field import FatcaField
from app.investment.business.customer.enums.occupation_code import OccupationCode
from app.investment.business.customer.enums.source_of_wealth_code import (
    SourceOfWealthCode,
)


class Fatca(InvestmentBaseModel):
    occupation_code: OccupationCode | None = None
    annual_income_code: AnnualIncomeCode | None = None
    source_of_wealth_code: SourceOfWealthCode | None = None

    birth_country: str = "IN"
    address_type: AddressType | None = None

    is_indian_tax_payer: bool | None = None
    politically_exposed: bool | None = None

    @property
    def is_complete(self) -> bool:
        return len(self.missing_fields) == 0

    @property
    def missing_fields(self) -> list[FatcaField]:
        missing: list[FatcaField] = []

        if self.occupation_code is None:
            missing.append(FatcaField.OCCUPATION)

        if self.annual_income_code is None:
            missing.append(FatcaField.ANNUAL_INCOME)

        if self.source_of_wealth_code is None:
            missing.append(FatcaField.SOURCE_OF_WEALTH)

        if not self.birth_country:
            missing.append(FatcaField.BIRTH_COUNTRY)

        if self.address_type is None:
            missing.append(FatcaField.ADDRESS_TYPE)

        if self.is_indian_tax_payer is None:
            missing.append(FatcaField.INDIAN_TAX_PAYER)

        if self.politically_exposed is None:
            missing.append(FatcaField.POLITICALLY_EXPOSED)

        return missing