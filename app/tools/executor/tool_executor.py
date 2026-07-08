# app/tools/executor/tool_executor.py

import time

from app.business.advisor.models.advisor_error import AdvisorError
from app.tools.executor.tool_execution_engine import ToolExecutionEngine
from app.tools.schemas.tool_request import ToolRequest
from app.tools.schemas.tool_response import ToolResponse
from app.tools.registry.tool_registry import ToolRegistry


class ToolExecutor(ToolExecutionEngine):
    def __init__(self, tool_registry: ToolRegistry):
        self.tool_registry = tool_registry

    async def execute(self, tool_name: str, request: ToolRequest) -> ToolResponse:
        start_time = time.perf_counter()

        try:
            tool = self.tool_registry.get_tool(tool_name=tool_name)

            response = await tool.execute(request)

            if response.execution_time_ms is None:
                response.execution_time_ms = round((time.perf_counter()-start_time)*1000)

            request.state.tool_results.append({
                "tool": tool_name,
                "success": response.success,
                "execution_time_ms": response.execution_time_ms
            })

            return response

        except Exception as ex:
            execution_time_ms = round((time.perf_counter() - start_time)*1000)

            request.state.errors.append(
                AdvisorError.from_exception(
                    exception=ex,
                    source=tool_name,
                    fatal=True
                )
            )
            
            request.state.tool_results.append(
                {
                    "tool": tool_name,
                    "success": False,
                    "execution_time_ms": execution_time_ms,
                }
            )

            request.state.metadata.setdefault("tools", []).append(
                {
                    "tool": tool_name,
                    "success": False,
                    "execution_time_ms": execution_time_ms,
                    "error": str(ex),
                }
            )

            return ToolResponse(
                success=False,
                error=str(ex),
                execution_time_ms=execution_time_ms
            )