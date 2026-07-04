from dataclasses import dataclass

from app.workflows.advisor.advisor_state import AdvisorState

@dataclass(slots=True)
class ToolRequest:
    state: AdvisorState