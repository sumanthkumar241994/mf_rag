from app.business.advisor.enums.tool_type import ToolType
from app.prompts.builder.advisor.sections.base_section import BaseSection
from app.workflows.advisor.advisor_state import AdvisorState


class DocumentSection(BaseSection):

    def build(
        self,
        state: AdvisorState,
    ) -> list[str]:

        if not self.tool_executed(state, ToolType.DOCUMENT_SEARCH):
            return []

        if not state.llm_context:
            return []

        lines: list[str] = []

        self.add_heading(lines, "Retrieved Document Context")

        lines.append(state.llm_context.context)

        self.add_blank_line(lines)

        return lines