# app/workflows/nodes/document_search_node.py

from app.workflows.advisor.advisor_state import AdvisorState
from app.tools.executor.tool_executor import ToolExecutor
from app.observability.tracing import trace_step

class DocumentSearchNode:
    def __init__(
        self,
        tool_executor: ToolExecutor
    ):
        self.tool_executor = tool_executor

    @trace_step("document_search")
    async def __call__(
        self,
        state: AdvisorState
    ) -> dict:
        tool_response = await self.tool_executor.execute(
            tool_name="document_search",
            arguments={
                "query": state['query']
            }
        )

        if not tool_response.success:
            raise RuntimeError(f"Document Search Failed: {tool_response.error}")
        
        return {
            "chunks": tool_response.result
        }

