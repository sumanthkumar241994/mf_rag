from app.business.advisor.planner.models.planner_validation_result import (
    PlannerValidationResult,
)
from app.business.advisor.planner.planner_parser import PlannerParser
from app.business.advisor.planner.planner_validator import PlannerValidator
from app.llm_gateway.enums.model_profile import ModelProfile
from app.llm_gateway.llm_gateway import LLMGateway
from app.prompts.planner.planner_prompt_builder import PlannerPromptBuilder
from app.workflows.advisor.advisor_state import AdvisorState


class PlannerService:

    def __init__(
        self,
        prompt_builder: PlannerPromptBuilder,
        llm_gateway: LLMGateway,
        parser: PlannerParser,
        validator: PlannerValidator,
    ):
        self._prompt_builder = prompt_builder
        self._llm_gateway = llm_gateway
        self._parser = parser
        self._validator = validator

    async def plan(
        self,
        state: AdvisorState,
    ) -> PlannerValidationResult:

        request = self._prompt_builder.build(state)

        response = await self._llm_gateway.generate(
            request=request,
            model_profile=ModelProfile.PLANNER,
        )

        planner = self._parser.parse(response.answer)

        return self._validator.validate(planner)