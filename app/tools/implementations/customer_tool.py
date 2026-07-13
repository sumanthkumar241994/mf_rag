from app.business.advisor.enums.tool_type import ToolType
from app.business.customer.customer_service import CustomerService
from app.tools.base.base_tool import BaseTool
from app.tools.schemas.tool_request import ToolRequest
from app.tools.schemas.tool_response import ToolResponse


class CustomerTool(BaseTool):
    def __init__(self, customer_service: CustomerService):
        self._customer_service = customer_service
    
    # async def execute(self, request: ToolRequest) -> ToolResponse:
    #     await self._customer_service.retrieve(request.state)

    #     return ToolResponse(
    #         success=request.state.customer is not None
    #     )
    async def execute(self, request: ToolRequest) -> ToolResponse:
        execution = await self._customer_service.retrieve(request.state)

        return ToolResponse(
            success= execution.result is not None
        )