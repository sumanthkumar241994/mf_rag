from app.business.advisor.enums.tool_type import ToolType
from app.prompts.builder.advisor.sections.base_section import BaseSection
from app.workflows.advisor.advisor_state import AdvisorState


class PortfolioSection(BaseSection):
    def build(self, state: AdvisorState) -> list[str]:
        if not self.tool_executed(state, ToolType.PORTFOLIO):
            return []

        lines: list[str] = []

        self.add_heading(lines, "Portfolio Analysis")

        lines.append(str(state.portfolio_analysis))

        self.add_blank_line(lines)

        return lines