# tools/registry/tool_registry.py

from collections import defaultdict
from app.business.advisor.enums.capabilities import Capability
from app.tools.base.base_tool import BaseTool
from app.tools.definitions.tool_definition import ToolDefinition
from app.tools.exceptions.tool_exceptions import CapabilityNotSupportedException, DuplicateToolRegistrationException, ToolDisabledException, ToolNotRegisteredException

class ToolRegistry:

    def __init__(self):
        self._definitions: dict[str, ToolDefinition] = {}
        self._tools: dict[str, BaseTool] = {}
        self._capability_index: dict[Capability, list[str]] = defaultdict(list)

    def register(self, definition: ToolDefinition, tool: BaseTool) -> None:
        if definition.name in self._definitions:
            raise DuplicateToolRegistrationException(definition.name)
        
        self._definitions[definition.name] = definition
        self._tools[definition.name] = tool

        self._capability_index[definition.capability].append(definition.name)

    def get_tool(self, tool_name: str ) -> BaseTool:
        if tool_name not in self._tools:
            raise ToolNotRegisteredException(tool_name)
        
        definition = self._definitions[tool_name]

        if not definition.enabled:
            raise ToolDisabledException(tool_name)

        return self._tools[tool_name]


    def get_tools_by_capability(self, capability: Capability) -> list[BaseTool]:
        tool_names = self._capability_index.get(capability)

        if not tool_names:
            raise CapabilityNotSupportedException(capability)

        return [self.get_tool(tool_name) for tool_name in tool_names]

    def get_definition(self, tool_name: str) -> ToolDefinition:
        if tool_name not in self._definitions:
            raise ToolNotRegisteredException(tool_name)
        
        return self._definitions[tool_name]

    def get_definitions_by_capability(self, capability: Capability) -> list[ToolDefinition]:
        tool_names = self._capability_index.get(capability)

        if not tool_names:
            raise CapabilityNotSupportedException(capability)
        
        return [self._definitions[tool_name] for tool_name in tool_names]
        
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
        
        definition = self._definitions.pop(tool_name)
        self._tools.pop(tool_name)

        self._capability_index[definition.capability].remove(tool_name)

        if not self._capability_index[definition.capability]:
            del self._capability_index[definition.capability]

    

    
