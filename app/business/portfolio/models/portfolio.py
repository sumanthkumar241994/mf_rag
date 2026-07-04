from dataclasses import dataclass
from datetime import datetime

from app.business.portfolio.models.category_allocation import CategoryAllocation
from app.business.portfolio.models.holding import Holding
from app.business.portfolio.models.investment_type_allocation import InvestmentTypeAllocation
from app.business.portfolio.models.portfolio_summary import PortfolioSummary
from app.business.portfolio.models.portfolio_totals import PortfolioTotals


@dataclass(slots=True)
class Portfolio:
    version: str
    generated_at: datetime
    generated_by: str
    totals: PortfolioTotals
    summary: PortfolioSummary
    category_allocation: dict[str, CategoryAllocation]
    investment_type_allocation: dict[str, InvestmentTypeAllocation]
    holdings: list[Holding]