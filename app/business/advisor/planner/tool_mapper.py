from app.business.advisor.enums.tool_type import ToolType
from app.business.advisor.models.capability_match import CapabilityMatch
from app.business.advisor.planner.rules.capability_tool_rules import CAPABILITY_TOOL_RULES


class ToolMapper:
    def map(self, capabilities: list[CapabilityMatch]) -> list[ToolType]:
        tools: list[ToolType] = []
        seen: set[ToolType] = set()

        for match in capabilities:
            mapped_tools = CAPABILITY_TOOL_RULES.get(match.capability, [])

            for tool in mapped_tools:
                if tool not in seen:
                    seen.add(tool)
                    tools.append(tool)

        return tools