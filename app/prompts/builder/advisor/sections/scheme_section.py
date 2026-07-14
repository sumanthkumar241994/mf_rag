from app.business.advisor.enums.tool_type import ToolType
from app.business.scheme.models.scheme_details import SchemeDetails
from app.prompts.builder.advisor.sections.base_section import BaseSection
from app.workflows.advisor.advisor_state import AdvisorState


class SchemeSection(BaseSection):
    def build(self, state: AdvisorState) -> list[str]:
        if not self.tool_executed(state, ToolType.SCHEME):
            return []

        lines: list[str] = []

        self.add_heading(lines, "Scheme Information")

        multiple = len(state.schemes) > 1

        for index, scheme in enumerate(state.schemes, start=1):

            if multiple:
                lines.append(f"### Scheme {index}")

            self._append_scheme(lines, scheme)

            lines.append("")

        return lines

    def _append_scheme(
        self,
        lines: list[str],
        scheme: SchemeDetails,
    ) -> None:

        self.add_field(lines, "Name", scheme.name)
        self.add_field(lines, "AMC", scheme.amc_name)
        self.add_field(lines, "Category", scheme.category)
        self.add_field(lines, "Sub Category", scheme.scheme_type)
        self.add_field(lines, "Investment Option", scheme.investment_option)

        self.add_field(lines, "NAV", scheme.nav)
        self.add_field(lines, "Expense Ratio", scheme.expense_ratio)
        self.add_field(lines, "Riskometer", scheme.riskometer)
        self.add_field(lines, "Rating", scheme.rating)
        self.add_field(lines, "AUM", scheme.aum)

        self.add_field(lines, "Fund Manager", scheme.fund_manager_name)
        self.add_field(lines, "Benchmark", scheme.benchmark)

        self.add_field(lines, "1 Year Return", scheme.one_year_return_percent)
        self.add_field(lines, "3 Year Return", scheme.three_months_return_percent)
        self.add_field(lines, "5 Year Return", scheme.five_years_return_percent)

        self.add_field(lines, "Minimum SIP", scheme.minimum_sip_amount)
        self.add_field(lines, "Minimum Lumpsum", scheme.minimum_initial_investment)

        self.add_field(lines, "Exit Load", scheme.exit_load)

        if scheme.objective:
            lines.append("Investment Objective:")
            lines.append(scheme.objective)

        if scheme.company_holdings:
            lines.append("")
            lines.append("Top Holdings:")

            for holding in scheme.company_holdings[:10]:
                lines.append(
                    f"- {holding.company_name}: {holding.holding_percentage}%"
                )

        if scheme.sectoral_holdings:
            lines.append("")
            lines.append("Sector Allocation:")

            for sector in scheme.sectoral_holdings[:10]:
                lines.append(
                    f"- {sector.sector}: {sector.allocation}%"
                )

        