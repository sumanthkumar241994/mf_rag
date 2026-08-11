from enum import StrEnum


class FatcaField(StrEnum):
    OCCUPATION = "occupation_code"
    ANNUAL_INCOME = "annual_income_code"
    SOURCE_OF_WEALTH = "source_of_wealth_code"
    BIRTH_COUNTRY = "birth_country"
    ADDRESS_TYPE = "address_type"
    INDIAN_TAX_PAYER = "is_indian_tax_payer"
    POLITICALLY_EXPOSED = "politically_exposed"