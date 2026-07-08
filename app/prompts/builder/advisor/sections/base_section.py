from abc import ABC, abstractmethod

from app.business.advisor.enums.tool_type import ToolType
from app.workflows.advisor.advisor_state import AdvisorState


class BaseSection(ABC):

    @abstractmethod
    def build(self, state: AdvisorState) -> list[str]:
        """
        Returns markdown lines for this section.

        Returns an empty list if the section is not applicable.
        """
        raise NotImplementedError
    
    @staticmethod
    def add_heading(lines: list[str], heading: str):
        lines.append(f"## {heading}")

    @staticmethod
    def add_blank_line(lines: list[str]):
        lines.append("")

    @staticmethod
    def tool_executed(state: AdvisorState, tool: ToolType) -> bool:
        return any(result['tool'] == tool.value and result['success'] for result in state.tool_results)

    @staticmethod
    def add_field(lines: list[str], label: str, value):
        if value is None:
            return
        
        if isinstance(value, str) and not value.strip():
            return
        
        lines.append(f"{label}: {value}")

    