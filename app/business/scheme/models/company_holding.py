from dataclasses import dataclass


@dataclass(slots=True)
class CompanyHolding:
    company_name: str
    sector: str | None
    holding_percentage: float
    market_value: float | None = None
    credit_rating: str | None = None