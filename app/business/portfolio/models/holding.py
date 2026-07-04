from dataclasses import dataclass, field
from typing import Any
from decimal import Decimal

from app.business.portfolio.enums import InvestmentType

from .scheme import Scheme

@dataclass(slots=True, frozen=True)
class Holding:
    group_id: str
    investment_type: InvestmentType
    folio_number: str | None

    invested_amount: Decimal
    current_value: Decimal
    gain: Decimal

    units: Decimal | None
    nav: Decimal | None
    average_nav: Decimal | None

    scheme: Scheme
    
    metadata: dict[str, Any] = field(default_factory=dict)

