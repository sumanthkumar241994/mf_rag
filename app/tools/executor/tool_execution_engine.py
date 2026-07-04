from abc import ABC, abstractmethod

from app.business.advisor.enums.tool_type import ToolType
from app.tools.schemas.tool_request import ToolRequest
from app.tools.schemas.tool_response import ToolResponse


class ToolExecutionEngine(ABC):
    """
    Abstraction for executing tools.

    Implementations may add retry, timeout,
    metrics, circuit breaker, etc.
    """

    @abstractmethod
    async def execute(
        self,
        tool_name: ToolType,
        request: ToolRequest,
    ) -> ToolResponse:
        raise NotImplementedError