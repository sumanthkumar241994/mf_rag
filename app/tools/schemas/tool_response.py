from dataclasses import dataclass
from typing import Any

@dataclass(slots=True)
class ToolResponse:
    success: bool
    result: Any = None
    error: str | None = None
    execution_time_ms: int | None = None