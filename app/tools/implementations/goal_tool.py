from app.business.advisor.enums.tool_type import ToolType
from app.business.goal.service.goal_service import GoalService
from app.tools.base.base_tool import BaseTool
from app.tools.schemas.tool_request import ToolRequest
from app.tools.schemas.tool_response import ToolResponse


class GoalTool(BaseTool):
    def __init__(self, goal_service: GoalService):
        self._goal_service = goal_service

    @property
    def tool_type(self) -> ToolType:
        return ToolType.GOAL
    
    async def execute(self, request: ToolRequest) -> ToolResponse:
        execution = await self._goal_service.analyze(request.state)

        return ToolResponse(
            success= execution.result is not None
        )