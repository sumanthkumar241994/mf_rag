from app.business.advisor.models.planner_result import PlannerResult
from app.business.advisor.planner.exceptions import PlannerParserError
from app.business.advisor.planner.planner import Planner
from app.business.advisor.planner.planner_service import PlannerService
from app.mapper.planner_result_mapper import PlannerResultMapper
from app.workflows.advisor.advisor_state import AdvisorState
import logging

logger = logging.getLogger(__name__)

class HybridPlanner(Planner):

    def __init__(
        self,
        planner_service: PlannerService,
        deterministic_planner: Planner,
        planner_result_mapper: PlannerResultMapper,
    ):
        self._planner_service = planner_service
        self._deterministic_planner = deterministic_planner
        self._planner_result_mapper = planner_result_mapper

    async def plan(
        self,
        state: AdvisorState,
    ) -> PlannerResult:

        try:
            return await self._llm_plan(state)

        except PlannerParserError as exc:
            logger.warning(
                "LLM planner parsing failed. Falling back to deterministic planner.",
                extra={"error": str(exc)},
            )
            return await self._fallback_plan(state)

    async def _llm_plan(
        self,
        state: AdvisorState,
    ) -> PlannerResult:
        try:
            result = await self._planner_service.plan(state)
            return result
            
        except Exception as exc:
            logger.exception(f"LLM planner failed. Falling back to deterministic planner. {str(exc)}")
            return await self._fallback_plan(state)

    async def _fallback_plan(
        self,
        state: AdvisorState,
    ) -> PlannerResult:

        return await self._deterministic_planner.plan(state)