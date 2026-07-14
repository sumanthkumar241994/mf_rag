from __future__ import annotations

from app.business.advisor.enums.agent_type import AgentType
from app.business.advisor.enums.capabilities import Capability
from app.business.advisor.enums.intent import Intent
from app.business.advisor.enums.tool_type import ToolType
from app.business.advisor.models.capability_match import CapabilityMatch
from app.business.advisor.models.planner_result import PlannerResult


class PlannerResultMapper:

    @staticmethod
    def from_dict(
        data: PlannerResult | dict | None,
    ) -> PlannerResult | None:

        if data is None:
            return None

        if isinstance(data, PlannerResult):
            return data

        return PlannerResult(
            intent=Intent(data["intent"]),
            capabilities=[
                PlannerResultMapper._capability_match(item)
                for item in data.get("capabilities", [])
            ],
            agent=AgentType(data["agent"]),
            selected_tools=[
                ToolType(tool)
                for tool in data.get("selected_tools", [])
            ],
            confidence=float(data.get("confidence", 1.0)),
            reasoning=data.get("reasoning"),
        )

    @staticmethod
    def _capability_match(
        data: CapabilityMatch | dict,
    ) -> CapabilityMatch:

        if isinstance(data, CapabilityMatch):
            return data

        return CapabilityMatch(
            capability=Capability(data["capability"]),
            confidence=float(data.get("confidence", 1.0)),
            matched_phrase=data.get("matched_phrase", ""),
            rule_priority=int(data.get("rule_priority", 0)),
        )