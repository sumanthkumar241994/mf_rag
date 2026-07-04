# from decimal import Decimal
# from typing import Any

# from business.portfolio.models import Holding, Scheme, Portfolio


# class PortfolioMappingError(Exception):
#     """Raised when Falcon portfolio response cannot be mapped."""


# class PortfolioMapper:
#     """Maps Falcon Portfolio API response into Portfolio domain models."""

#     @classmethod
#     def from_falcon_response(cls, response: dict[str, Any]) -> Portfolio:
#         """
#         Convert Falcon Portfolio API response into Portfolio domain model.
#         """

#         try:
#             totals = response['totals']
#             category_totals = response['category_totals']
#             holdings = [cls._map_holding(item) for item in response.get("investments", [])]

#             return Portfolio(
#                 total_value=cls._decimal(totals['current_value']),
#                 total_investment=cls._decimal(totals['net_investment']),
#                 total_gain=cls._decimal(totals['net_gain']),
#                 equity_value=cls._decimal(category_totals['equity']),
#                 debt_value=cls._decimal(category_totals['debt']),
#                 other_value=cls._decimal(category_totals['others']),
#                 holdings=holdings
#             )

#         except KeyError as ex:
#             raise PortfolioMappingError(f"Missing required field: {ex}") from ex
#         except Exception as ex:
#             raise PortfolioMappingError(f"unable to map the portfolio response: {str(ex)}") from ex

#     @classmethod
#     def _map_holding(cls, data: dict[str, Any]) -> Holding:
#         return Holding(
#             group_id=data['group_id'],
#             investment_type=data['investment_type'],
#             display_name=data['display_name'],
#             folio_number=data['folio_number'],
#             has_folio=data['has_folio'],
#             invested_amount=cls._decimal(data['i_net_investment']),
#             current_value=cls._decimal(data['i_current_value'],
#             gain=cls._decimal(data['p_net_gain']),
#             units=cls._optional_decimal(data['units']),
#             nav=cls._optional_decimal(data['nav']),
#             average_nav=cls._optional_decimal(data['avg_nav']),
#             scheme = cls._map_scheme(data['scheme']),
#             metadata={
#                 "exit_load": data.get("exit_load"),
#                 "stcg": data.get("stcg"),
#                 "ltcg": data.get("ltcg"),
#                 "can_switch": data.get("can_switch"),
#                 "next_transaction_on": data.get("next_transaction_on"),

#                 }
#             )
#         )
    
#     @classmethod
#     def _map_scheme(cls, data: dict[str, Any]) -> Scheme:
#         return Scheme(
#             id=data['id'],
#             isin=data['isin'],
#             name=data['name'],
#             short_name=data['short_name'],
#             category=data['category'],
#             scheme_type=data['scheme_type'],
#             rating=data.get['rating'],
#             minimum_initial_investment=cls._decimal(data.get('minimum_initial_investment')),
#             minimum_sip_amount=cls._optional_decimal(data.get("minimum_sip_amount"))
#         )

#     @staticmethod
#     def _decimal(value: Any) -> Decimal:
#         if value is None:
#             return Decimal("0")

#         return Decimal(value)
    
#     @staticmethod
#     def _optional_decimal(value: Any) -> Decimal | None:
#         if value is None:
#             return None
#         return Decimal(value)


from decimal import Decimal
from datetime import datetime

from app.business.portfolio.models.category_allocation import CategoryAllocation
from app.business.portfolio.models.category_allocations import CategoryAllocations
from app.business.portfolio.models.holding import Holding
from app.business.portfolio.models.investment_type_allocation import InvestmentTypeAllocation
from app.business.portfolio.models.investment_type_allocations import InvestmentTypeAllocations
from app.business.portfolio.models.portfolio import Portfolio
from app.business.portfolio.models.portfolio_summary import (
    LargestHoldingSummary,
    PortfolioSummary,
)
from app.business.portfolio.models.portfolio_totals import PortfolioTotals
from app.business.portfolio.models.scheme import Scheme
from app.business.portfolio.models.sector_holding import SectorHolding


class PortfolioMapper:

    @classmethod
    def from_falcon_response(
        cls,
        payload: dict,
    ) -> Portfolio:

        return Portfolio(
            version=payload["portfolio_version"],
            generated_at=cls._parse_datetime(payload["generated_at"]),
            generated_by=payload["generated_by"],
            totals=cls._map_totals(payload["totals"]),
            summary=cls._map_summary(payload["summary"]),
            category_allocation=cls._map_category_allocations(payload["category_allocation"]),
            investment_type_allocation=cls._map_investment_allocations(
                payload["investment_type_allocation"]
            ),
            holdings=[
                cls._map_holding(item)
                for item in payload["investments"]
            ],
        )

    # ---------------------------------------------------------

    @staticmethod
    def _map_totals(
        payload: dict,
    ) -> PortfolioTotals:

        return PortfolioTotals(
            current_value=Decimal(str(payload["current_value"])),
            net_investment=Decimal(str(payload["net_investment"])),
            net_gain=Decimal(str(payload["net_gain"])),
            return_percentage=Decimal(str(payload["return_percentage"])),
            folio_count=payload["folio_count"],
            holding_count=payload["holding_count"],
            scheme_count=payload["scheme_count"],
            amc_count=payload["amc_count"],
        )

    # ---------------------------------------------------------

    @staticmethod
    def _map_summary(
        payload: dict,
    ) -> PortfolioSummary:

        largest = payload.get("largest_holding")

        return PortfolioSummary(
            largest_holding=(
                LargestHoldingSummary(
                    scheme_name=largest["scheme_name"],
                    scheme_code=largest["scheme_code"],
                    category=largest["category"],
                    amc_name=largest["amc_name"],
                    current_value=Decimal(str(largest["current_value"])),
                    allocation_percentage=Decimal(str(largest["allocation_percentage"])),
                )
                if largest
                else None
            ),
            highest_risk_category=payload.get("highest_risk_category"),
            highest_exposure_amc=payload.get("highest_exposure_amc"),
            highest_exposure_amc_percentage=Decimal(str(payload.get("highest_exposure_amc_percentage",0)))
        )

    # ---------------------------------------------------------

    @staticmethod
    def _map_category(
        payload: dict,
    ) -> CategoryAllocation:

        return CategoryAllocation(
            current_value=Decimal(str(payload["current_value"])),
            invested_value=Decimal(str(payload["invested_value"])),
            gain=Decimal(str(payload["gain"])),
            allocation_percentage=Decimal(
                str(payload["allocation_percentage"])
            ),
        )

    @staticmethod
    def _map_category_allocations(
        payload: dict,
    ) -> CategoryAllocations:

        return CategoryAllocations(
            equity=PortfolioMapper._map_category(payload["equity"]),
            debt=PortfolioMapper._map_category(payload["debt"]),
            hybrid=PortfolioMapper._map_category(payload["hybrid"]),
            solution=PortfolioMapper._map_category(payload["solution"]),
            others=PortfolioMapper._map_category(payload["others"]),
        )

    # ---------------------------------------------------------

    @staticmethod
    def _map_investment_type(
        payload: dict,
    ) -> InvestmentTypeAllocation:

        return InvestmentTypeAllocation(
            current_value=Decimal(str(payload["current_value"])),
            invested_value=Decimal(str(payload["invested_value"])),
            gain=Decimal(str(payload["gain"])),
            allocation_percentage=Decimal(
                str(payload["allocation_percentage"])
            ),
        )

    @staticmethod
    def _map_investment_allocations(
        payload: dict,
    ) -> InvestmentTypeAllocations:

        return InvestmentTypeAllocations(
            sip=PortfolioMapper._map_investment_type(payload["sip"]),
            lumpsum=PortfolioMapper._map_investment_type(payload["lumpsum"]),
        )

    # ---------------------------------------------------------

    @classmethod
    def _map_holding(
        cls,
        payload: dict,
    ) -> Holding:

        return Holding(
            group_id=payload["group_id"],
            investment_type=payload["investment_type"],
            folio_number=payload.get("folio_number"),
            units=Decimal(str(payload["units"])),
            average_nav=Decimal(str(payload["avg_nav"])),
            nav=Decimal(str(payload["nav"])),
            current_value=Decimal(str(payload["p_current_value"])),
            invested_amount=Decimal(str(payload["p_net_investment"])),
            gain=Decimal(str(payload["p_net_gain"])),
            scheme=cls._map_scheme(payload["scheme"]),
        )

    # ---------------------------------------------------------

    @classmethod
    def _map_scheme(
        cls,
        payload: dict,
    ) -> Scheme:

        return Scheme(
            id=payload["id"],
            scheme_code=payload["scheme_code"],
            isin=payload["isin"],
            name=payload["name"],
            short_name=payload.get("short_name"),
            category=payload["category"],
            scheme_type=payload["scheme_type"],
            amc_name=payload["amc_name"],
            benchmark=payload.get("benchmark"),
            rating=payload.get("rating"),
            riskometer=payload["riskometer"],
            riskometer_display=payload["riskometer_display"],
            expense_ratio=Decimal(str(payload["expense_ratio"])),
            aum=Decimal(str(payload["aum"])),
            fund_manager_name=payload.get("fund_manager_name"),
            fund_manager_since=cls._parse_datetime(payload.get("fund_manager_since")),
            nav_last_updated_on=cls._parse_datetime(payload.get("nav_last_updated_on")),
            exit_load_percent=Decimal(str(payload["exit_load_percent"])),
            lock_in_period_days=payload["lock_in_period_days"],
            one_year_return=Decimal(str(payload["one_year_return"])) if payload.get("one_year_return") is not None else None,
            three_year_return=Decimal(str(payload["three_years_return"])) if payload.get("three_years_return") is not None else None,
            five_year_return=Decimal(str(payload["five_years_return"])) if payload.get("five_years_return") is not None else None,
            sector_holdings=cls._map_sector_holdings(payload.get("sectoral_holdings",[])),
        )

    # ---------------------------------------------------------

    @staticmethod
    def _map_sector_holdings(
        payload: list[dict],
    ) -> list[SectorHolding]:

        holdings = []

        for sector in payload:

            allocation = sector.get("allocation")

            try:
                allocation = Decimal(str(allocation)) if allocation not in ("",None) else Decimal("0")
            except Exception:
                allocation = Decimal("0")

            holdings.append(SectorHolding(sector=sector["display_name"],allocation=allocation))

        return holdings

    @staticmethod
    def _parse_datetime(value: str | None) -> datetime | None:
        if not value:
            return None
        return datetime.fromisoformat(value)