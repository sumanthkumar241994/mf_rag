from dataclasses import dataclass, field
from datetime import datetime
from decimal import Decimal

from app.business.portfolio.enums import SchemeCategory
from app.business.portfolio.models.sector_holding import SectorHolding


@dataclass(slots=True)
class Scheme:
    id: int
    scheme_code: str
    isin: str
    name: str
    short_name: str | None
    category: SchemeCategory
    scheme_type: str
    amc_name: str
    benchmark: str | None
    rating: int | None
    riskometer: int | None
    riskometer_display: str | None
    expense_ratio: Decimal | None
    aum: Decimal | None
    fund_manager_name: str | None
    fund_manager_since: datetime | None
    nav_last_updated_on: datetime | None
    exit_load_percent: Decimal
    lock_in_period_days: int
    one_year_return: Decimal | None
    three_year_return: Decimal | None
    five_year_return: Decimal | None
    sector_holdings: list[SectorHolding] = field(
        default_factory=list
    )