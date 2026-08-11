from app.business.advisor.planner.hybrid_planner import HybridPlanner
from app.business.advisor.planner.planner_parser import PlannerParser
from app.business.advisor.planner.planner_service import PlannerService
from app.business.advisor.planner.planner_validator import PlannerValidator
from app.composition.planner.deterministic_planner_composition import DeterministicPlannerComposition
from app.llm_gateway.llm_gateway import LLMGateway
from app.mapper.planner_result_mapper import PlannerResultMapper
from app.prompts.planner.planner_prompt_builder import PlannerPromptBuilder


class HybridPlannerComposition:

    def __init__(
        self,
        llm_gateway: LLMGateway,
    ):
        # Reuse deterministic planner
        self.deterministic = DeterministicPlannerComposition()

        # Prompt Builder
        self.prompt_builder = PlannerPromptBuilder()

        # Parser
        self.parser = PlannerParser()

        # Validator
        self.validator = PlannerValidator()

        # Planner Service
        self.planner_service = PlannerService(
            prompt_builder=self.prompt_builder,
            llm_gateway=llm_gateway,
            parser=self.parser,
            validator=self.validator,
            tool_mapper=self.deterministic.tool_mapper
        )

        # Result Mapper
        # self.planner_result_mapper = PlannerResultMapper(
        #     tool_mapper=self.deterministic.tool_mapper,
        # )
        self.planner_result_mapper = PlannerResultMapper()

        # Planner
        self.planner = HybridPlanner(
            planner_service=self.planner_service,
            deterministic_planner=self.deterministic.planner,
            planner_result_mapper=self.planner_result_mapper,
        )