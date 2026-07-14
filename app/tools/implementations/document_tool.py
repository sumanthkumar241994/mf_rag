from app.business.advisor.enums.tool_type import ToolType
from app.business.document.document_service import DocumentService
from app.tools.base.base_tool import BaseTool
from app.tools.schemas.tool_request import ToolRequest
from app.tools.schemas.tool_response import ToolResponse


class DocumentTool(BaseTool):
    def __init__(self, document_service: DocumentService):
        self._document_service = document_service

    @property
    def tool_type(self) -> ToolType:
        return ToolType.DOCUMENT_SEARCH
    
    async def execute(self, request: ToolRequest) -> ToolResponse:
        execution = await self._document_service.retrieve(request.state)

        return ToolResponse(
            success=execution is not None and execution.result is not None
        )