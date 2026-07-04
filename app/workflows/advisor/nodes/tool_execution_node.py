from typing import AsyncIterator
from app.dtos.agents.stream_event import AgentStreamEvent
from app.enums.stream_event_type import StreamEventType
from app.tools.executor.tool_execution_engine import ToolExecutionEngine
from app.workflows.advisor.advisor_state import AdvisorState


class ToolExecutionNode:
    """
    Executes all tools selected by the planner.
    Each tool enriches the shared AdvisorState.
    """

    def __init__(self, execution_engine: ToolExecutionEngine):
        self._execution_engine = execution_engine
    
    async def __call__(self, state: AdvisorState) -> AdvisorState:
        planner_result = state.planner_result

        if planner_result is None:
            return state
        
        for tool in planner_result.selected_tools:
            await self._execution_engine.execute(
                tool_name=tool,
                state=state
            )
        
        return state

    async def stream(self, state: AdvisorState) -> AsyncIterator[AgentStreamEvent]:
        planner_result = state.planner_result

        if planner_result is None:
            return 

        for tool in planner_result.selected_tools:

            yield AgentStreamEvent(
                type=StreamEventType.TOOL_START.value, tool=tool
            )

            await self._execution_engine.execute(
                tool_name=tool,
                state=state
            )

            tool_result = state.tool_results[-1]

            if isinstance(tool_result, dict):
                success = tool_result['success']
                execution_time_ms = tool_result['execution_time_ms']
            else:
                success = tool_result.success
                execution_time_ms = tool_result.execution_time_ms
            
            yield AgentStreamEvent(
                type=StreamEventType.TOOL_END.value,
                tool=tool,
                success=success,
                metadata={
                    "execution_time_ms": execution_time_ms
                }
            )