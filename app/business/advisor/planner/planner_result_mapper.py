from app.business.advisor.models.planner_result import PlannerResult
from app.business.advisor.planner.models.planner_response import PlannerResponse
from app.business.advisor.planner.tool_mapper import ToolMapper


class PlannerResultMapper:

    def __init__(
        self,
        tool_mapper: ToolMapper,
    ):
        self._tool_mapper = tool_mapper

    def map(
        self,
        planner: PlannerResponse,
    ) -> PlannerResult:

        return PlannerResult(
            intent=planner.intent,
            capabilities=planner.capabilities,
            selected_tools=self._tool_mapper.map(
                planner.capabilities
            ),
            confidence=planner.confidence,
            reasoning="\n".join(
                reason.reason
                for reason in planner.reasons
            ),
        )