from app.business.advisor.enums.tool_type import ToolType
from app.business.scheme.scheme_service import SchemeService
from app.tools.base.base_tool import BaseTool
from app.tools.schemas.tool_request import ToolRequest
from app.tools.schemas.tool_response import ToolResponse


class SchemeTool(BaseTool):
    def __init__(self, scheme_service: SchemeService):
        self._scheme_service = scheme_service
    
    # async def execute(self, request: ToolRequest) -> ToolResponse:
    #     await self._scheme_service.execute(request.state)

    #     return ToolResponse(
    #         success=request.state.schemes is not None
    #     )
    
    async def execute(self, request: ToolRequest) -> ToolResponse:
        execution = await self._scheme_service.execute(request.state)

        return ToolResponse(
            success=execution is not None and execution.result is not None
        )