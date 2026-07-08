from dataclasses import dataclass, field
from datetime import datetime

from app.business.scheme.models.company_holding import CompanyHolding
from app.business.scheme.models.exit_load import ExitLoad
from app.business.scheme.models.sector_holding import SectorHolding


@dataclass(slots=True)
class SchemeDetails:
    # Identity
    id: int
    mstar_parent_id: str |None
    amfi_code: str | None

    name: str
    short_name: str | None

    amc_code: str
    amc_name: str

    category: str
    scheme_type: str

    investment_option: str | None

    is_direct: bool
    status: bool

    isin: str | None

    # Investment Profile
    objective: str | None
    benchmark: str | None
    inception_date: datetime | None

    # Fund Metrics
    nav: float | None
    nav_last_updated_on: datetime | None
    nav_day_change: float | None

    aum: float | None
    aum_date: datetime | None

    expense_ratio: float | None

    rating: int

    riskometer: int | None
    riskometer_display: str | None

    fund_manager_name: str | None
    fund_manager_since: datetime | None

    # Returns
    one_month_return_percent: float | None
    three_months_return_percent: float | None
    six_months_return_percent: float | None

    one_year_return_percent: float | None
    three_years_return_percent: float | None
    five_years_return_percent: float | None

    returns_updated_on: datetime | None

    # Transaction Rules
    minimum_initial_investment: float | None
    minimum_subsequent_investment: float | None
    minimum_sip_amount: float | None

    sip_allowed: bool
    lumpsum_allowed: bool

    switch_allowed: bool

    stp_allowed: bool
    swp_allowed: bool

    redemption_allowed: bool

    lock_in_period_days: int | None

    exit_load: float | None
    exit_load_age_days: int | None
    max_exit_load_percentage: float | None

    exit_loads: list[ExitLoad] = field(default_factory=list)

    # Asset Allocation
    asset_alloc_equity: float | None = None
    asset_alloc_debt: float | None = None
    asset_alloc_cash: float | None = None

    # Portfolio
    portfolio_date: datetime | None = None

    company_holdings: list[CompanyHolding] = field(default_factory=list)
    sectoral_holdings: list[SectorHolding] = field(default_factory=list)