from app.tools.executor.retry_executor import RetryExecutor
from app.tools.executor.tool_executor import ToolExecutor
from app.tools.registry.tool_registry import ToolRegistry


class ToolComposition:
    def __init__(self):
        self.registry = ToolRegistry()

        self.tool_executor = ToolExecutor(
            tool_registry=self.registry
        )

        self.execution_engine = RetryExecutor(
            tool_executor=self.tool_executor,
            retry_policy=None
        )