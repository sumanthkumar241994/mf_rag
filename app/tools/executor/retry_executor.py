import asyncio
from app.tools.executor.tool_execution_engine import ToolExecutionEngine
from app.tools.retry.retry_policy import RetryPolicy
from app.business.advisor.enums.tool_type import ToolType
from app.tools.executor.tool_executor import ToolExecutor
from app.tools.schemas.tool_request import ToolRequest
from app.tools.schemas.tool_response import ToolResponse
from app.workflows.advisor.advisor_state import AdvisorState


class RetryExecutor(ToolExecutionEngine):
    """
    Adds retry capability on top of ToolExecutor.

    RetryExecutor does not know anything about individual tools.
    It simply retries failed executions according to RetryPolicy.
    """
    def __init__(
        self,
        tool_executor: ToolExecutor,
        retry_policy: RetryPolicy | None = None
    ):
        self._tool_executor = tool_executor
        self._retry_policy = retry_policy or RetryPolicy()

    async def execute(self, tool_name: ToolType, state: AdvisorState) -> ToolResponse:
        response: ToolResponse | None = None

        for attempt in range(1, self._retry_policy.max_attempts + 1):
            response = await self._tool_executor.execute(
                tool_name=tool_name.value,
                request=ToolRequest(
                    state=state
                )
            )

            if response.success:
                state.clear_error(tool_name.value)
                return response
            
            latest_error = state.get_latest_error(tool_name.value)

            if latest_error is None: 
                return response

            if not latest_error.retryable:
                return response

            if attempt >= self._retry_policy.max_attempts:
                return response

            latest_error.retry_count += 1

            delay = self._calculate_delay(attempt)
            await asyncio.sleep(delay)
        
        return response
    

    def _calculate_delay(self, attempt: int) -> float:
        if not self._retry_policy.exponential_backoff:
            return self._retry_policy.base_delay_seconds
        
        return self._retry_policy.base_delay_seconds * (2** (attempt -1))
