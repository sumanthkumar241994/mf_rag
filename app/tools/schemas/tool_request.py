from dataclasses import dataclass

@dataclass(slots=True)
class ToolRequest:
    tool_name: str
    arguments: dict