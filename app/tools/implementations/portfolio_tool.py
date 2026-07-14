from app.business.portfolio.service.portfolio_service import PortfolioService
from app.tools.base.base_tool import BaseTool
from app.tools.schemas.tool_request import ToolRequest
from app.tools.schemas.tool_response import ToolResponse


class PortfolioTool(BaseTool):
    def __init__(self, portfolio_service: PortfolioService):
        self._portfolio_service = portfolio_service
    
    # async def execute(self, request: ToolRequest) -> ToolResponse:
    #     await self._portfolio_service.analyze(request.state)

    #     return ToolResponse(
    #         success=request.state.portfolio_analysis is not None
    #     )

    async def execute(self, request: ToolRequest) -> ToolResponse:
        execution = await self._portfolio_service.analyze(request.state)

        return ToolResponse(
            success=execution is not None and execution.result is not None
        )