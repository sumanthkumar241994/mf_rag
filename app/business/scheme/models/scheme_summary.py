from dataclasses import dataclass


@dataclass(slots=True)
class SchemeSummary:
    id: int
    mstar_parent_id: str | None

    name: str
    short_name: str | None

    amc_code: str
    amc_name: str

    category: str
    scheme_type: str

    investment_option: str | None

    is_direct: bool
    status: bool

    minimum_initial_investment: float | None
    minimum_sip_amount: float | None

    riskometer: int | None
    riskometer_display: str | None

    aum: float | None

    rating: int

    lock_in_period_days: int | None

    sip_allowed: bool
    lumpsum_allowed: bool
    redemption_allowed: bool
    switch_allowed: bool

    amfi_code: str | None
    isin: str | None

    one_year_return_percent: float | None
    three_years_return_percent: float | None
    five_years_return_percent: float | None