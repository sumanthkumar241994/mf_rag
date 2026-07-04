from dataclasses import dataclass

from app.business.advisor.enums.tool_type import ToolType


@dataclass(slots=True)
class ToolExecutionResult:
    tool: ToolType
    success: bool
    execution_time_ms: int