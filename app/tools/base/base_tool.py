from abc import ABC, abstractmethod

from app.tools.schemas.tool_request import ToolRequest
from app.tools.schemas.tool_response import ToolResponse

class BaseTool(ABC):

    @abstractmethod
    async def execute(
        self,
        request: ToolRequest
    ) -> ToolResponse:
        """
        Execute tool

        Returns standardised ToolResponse.
        """
        pass