# app/tools/executor/tool_executor.py

import time
from tracemalloc import start 

from app.tools.schemas.tool_request import ToolRequest
from app.tools.schemas.tool_response import ToolResponse
from app.tools.registry.tool_registry import ToolRegistry


class ToolExecutor:
    def __init__(self, tool_registry: ToolRegistry):
        self.tool_registry = tool_registry

    async def execute(self, tool_name: str, arguments: dict | None = None) -> ToolResponse:
        start_time = time.perf_counter()

        try:
            tool = self.tool_registry.get_tool(tool_name=tool_name)
            request = ToolRequest(
                tool_name=tool_name,
                arguments=arguments or {}
            )

            response = await tool.execute(request)

            if response.execution_time_ms is None:
                response.execution_time_ms = round((time.perf_counter()-start_time)*1000)
            
            return response
        except Exception as ex:
            execution_time_ms = round((time.perf_counter() - start_time)*1000)

            return ToolResponse(
                success=False,
                error=str(ex),
                execution_time_ms=execution_time_ms
            )