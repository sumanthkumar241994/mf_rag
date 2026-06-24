# app/tools/implementations/document_search_tool.py

import time

from app.tools.base.base_tool import BaseTool
from app.tools.schemas.tool_response import ToolResponse
from app.tools.schemas.tool_request import ToolRequest
from app.retrieval.retrieval_service import RetrievalService


class DocumentSearchTool(BaseTool):
    def __init__(
        self,
        retrieval_service: RetrievalService
    ):
        self.retrieval_service = retrieval_service

    async def execute(self, request: ToolRequest) -> ToolResponse:
        start_time = time.perf_counter()

        try:
            query = request.arguments['query']
            chunks = await self.retrieval_service.retrieve(query=query)
            execution_time_ms = round((time.perf_counter() - start_time) * 1000)

            return ToolResponse(
                success=True,
                result=chunks,
                execution_time_ms=execution_time_ms
            )
        except Exception as ex:
            execution_time_ms = round((time.perf_counter() - start_time)*1000)

            return ToolResponse(
                success=False,
                error=str(ex),
                execution_time_ms=execution_time_ms
            )
