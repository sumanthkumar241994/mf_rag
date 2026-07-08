from app.business.scheme.models.company_holding import CompanyHolding
from app.business.scheme.models.exit_load import ExitLoad
from app.business.scheme.models.scheme_details import SchemeDetails
from app.business.scheme.models.scheme_summary import SchemeSummary
from app.business.scheme.models.sector_holding import SectorHolding


class SchemeMapper:

    # ------------------------------------------------------------------
    # Search
    # ------------------------------------------------------------------

    @staticmethod
    def to_summary(data: dict) -> SchemeSummary:
        return SchemeSummary(
            id=data["id"],
            mstar_parent_id=data.get("mstar_parent_id"),
            name=data["name"],
            short_name=data.get("short_name"),
            amc_code=data["amc_code"],
            amc_name=data["amc_name"],
            category=data["category"],
            scheme_type=data["scheme_type"],
            investment_option=data.get("investment_option"),
            is_direct=data["is_direct"],
            status=data["status"],
            minimum_initial_investment=data.get("minimum_initial_investment"),
            minimum_sip_amount=data.get("minimum_sip_amount"),
            riskometer=data.get("riskometer"),
            riskometer_display=data.get("riskometer_display"),
            aum=data.get("aum"),
            rating=data.get("rating", 0),
            lock_in_period_days=data.get("lock_in_period_days"),
            sip_allowed=data.get("sip_allowed", False),
            lumpsum_allowed=data.get("lumpsum_allowed", False),
            redemption_allowed=data.get("redemption_allowed", False),
            switch_allowed=data.get("switch_allowed", False),
            amfi_code=data.get("amfi_code"),
            isin=data.get("isin"),
            one_year_return_percent=data.get("one_year_return_percent"),
            three_years_return_percent=data.get("three_years_return_percent"),
            five_years_return_percent=data.get("five_years_return_percent"),
        )

    @classmethod
    def to_summary_list(cls, data: list[dict]) -> list[SchemeSummary]:
        return [cls.to_summary(item) for item in data]

    # Details
    @staticmethod
    def to_details(data: dict) -> SchemeDetails:

        company_holdings = [
            SchemeMapper._map_company_holding(item)
            for item in data.get("company_holdings", [])
        ]

        sector_holdings = [
            holding
            for item in data.get("sectoral_holdings", []) 
            if (holding := SchemeMapper._map_sector_holding(item)) is not None
        ]

        exit_loads = [
            SchemeMapper._map_exit_load(item)
            for item in data.get("exit_loads", [])
        ]

        return SchemeDetails(

            #
            # Identity
            #
            id=data["id"],
            mstar_parent_id=data.get("mstar_parent_id"),
            amfi_code=data.get("amfi_code"),

            name=data["name"],
            short_name=data.get("short_name"),

            amc_code=data["amc_code"],
            amc_name=data["amc_name"],

            category=data["category"],
            scheme_type=data["scheme_type"],

            investment_option=data.get("investment_option"),

            is_direct=data["is_direct"],
            status=data["status"],

            isin=data.get("isin"),

            #
            # Investment Profile
            #
            objective=data.get("objective"),
            benchmark=data.get("benchmark"),
            inception_date=data.get("inception_date"),

            #
            # Fund Metrics
            #
            nav=data.get("nav"),
            nav_last_updated_on=data.get("nav_last_updated_on"),
            nav_day_change=data.get("nav_day_change"),

            aum=data.get("aum"),
            aum_date=data.get("aum_date"),

            expense_ratio=data.get("expense_ratio"),

            rating=data.get("rating", 0),

            riskometer=data.get("riskometer"),
            riskometer_display=data.get("riskometer_display"),

            fund_manager_name=data.get("fund_manager_name"),
            fund_manager_since=data.get("fund_manager_since"),

            #
            # Returns
            #
            one_month_return_percent=data.get("one_month_return_percent"),
            three_months_return_percent=data.get("three_months_return_percent"),
            six_months_return_percent=data.get("six_months_return_percent"),

            one_year_return_percent=data.get("one_year_return_percent"),
            three_years_return_percent=data.get("three_years_return_percent"),
            five_years_return_percent=data.get("five_years_return_percent"),

            returns_updated_on=data.get("returns_updated_on"),

            #
            # Transactions
            #
            minimum_initial_investment=data.get("minimum_initial_investment"),
            minimum_subsequent_investment=data.get(
                "minimum_subsequent_investment"
            ),
            minimum_sip_amount=data.get("minimum_sip_amount"),

            sip_allowed=data.get("sip_allowed", False),
            lumpsum_allowed=data.get("lumpsum_allowed", False),

            switch_allowed=data.get("switch_allowed", False),

            stp_allowed=data.get("stp_allowed", False),
            swp_allowed=data.get("swp_allowed", False),

            redemption_allowed=data.get("redemption_allowed", False),

            lock_in_period_days=data.get("lock_in_period_days"),

            exit_load=data.get("exit_load"),
            exit_load_age_days=data.get("exit_load_age_days"),
            max_exit_load_percentage=data.get("max_exit_load_percentage"),

            exit_loads=exit_loads,

            #
            # Asset Allocation
            #
            asset_alloc_equity=data.get("asset_alloc_equity"),
            asset_alloc_debt=data.get("asset_alloc_debt"),
            asset_alloc_cash=data.get("asset_alloc_cash"),

            #
            # Portfolio
            #
            portfolio_date=data.get("portfolio_date"),

            company_holdings=company_holdings,
            sectoral_holdings=sector_holdings,
        )

    # ------------------------------------------------------------------
    # Nested Models
    # ------------------------------------------------------------------

    @staticmethod
    def _map_company_holding(data: dict) -> CompanyHolding:
        return CompanyHolding(
            company_name=data["company_name"],
            sector=data.get("sector"),
            holding_percentage=data["weightage"],
            market_value=data.get("market_value"),
            credit_rating=data.get("credit_rating"),
        )

    @staticmethod
    def _map_sector_holding(data: dict) -> SectorHolding:
        if data['allocation'] !="":
            return SectorHolding(
                sector=data["display_name"],
                allocation=data["allocation"],
            )

    @staticmethod
    def _map_exit_load(data: dict) -> ExitLoad:
        return ExitLoad(
            percentage=data["Value"]
        )