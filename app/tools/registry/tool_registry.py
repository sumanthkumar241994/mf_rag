# tools/registry/tool_registry.py

from app.tools.base.base_tool import BaseTool
from app.tools.definitions.tool_definition import ToolDefinition

class ToolRegistry:

    def __init__(self):
        self._definitions: dict[str, ToolDefinition] = {}
        self._tools: dict[str, BaseTool] = {}

    def register(self, definition: ToolDefinition, tool: BaseTool) -> None:
        if definition.name in self._definitions:
            raise ValueError(
                f"Tool {definition.name} is already registered"
            )
        
        self._definitions[definition.name] = definition
        self._tools[definition.name] = tool


    def get_tool(self, tool_name: str ) -> BaseTool:
        if tool_name not in self._tools:
            raise ValueError(
                f"Tool {tool_name} is not registered"
            )
        
        definition = self._definitions[tool_name]

        if not definition.enabled:
            raise ValueError(f"Tool {tool_name} is not enabled")

        return self._tools[tool_name]
    
    def get_definition(self, tool_name: str) -> ToolDefinition:
        if tool_name not in self._definitions:
            raise ValueError(f"Tool {tool_name} is not registered")
        
    def is_registered(self, tool_name: str) -> bool:
        return tool_name in self._definitions

    def list_tools(self, enabled_only: bool = True) -> list[ToolDefinition]:
        tools = self._definitions.values()
        if enabled_only:
            return [tool for tool in tools if tool.enabled]

        return list(tools)

    def unregister(self, tool_name: str) -> None:
        if tool_name not in self._definitions:
            return
        
        del self._definitions[tool_name]
        del self._tools[tool_name]

    

    
