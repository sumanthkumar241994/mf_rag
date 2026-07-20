from dataclasses import asdict
from app.business.advisor.planner.exceptions import PlannerParserError
from app.business.advisor.planner.models.planner_error import PlannerError
from app.business.advisor.planner.models.planner_validation_result import (
    PlannerValidationResult,
)
from app.business.advisor.planner.planner_parser import PlannerParser
from app.business.advisor.planner.planner_validator import PlannerValidator
from app.llm_gateway.enums.model_profile import ModelProfile
from app.llm_gateway.llm_gateway import LLMGateway
from app.llm_gateway.model_profiles import MODEL_PROFILES
from app.observability.tracing import trace_step
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

    @trace_step(
        "llm_planner",
        input_mapper=lambda self, state: {
            "query": state.request.query,
        },
        output_mapper=lambda validation: (
            {
                "valid": False,
                "errors": [asdict(error) for error in validation.errors],
            }
            if not validation.valid
            else {
                "valid": True,
                "intent": validation.response.intent.value,
                "capabilities": [
                    {
                        "capability": c.capability.value,
                        "confidence": c.confidence,
                    }
                    for c in validation.response.capabilities
                ],
                "selected_tools": [
                    tool.value for tool in validation.response.selected_tools
                ],
                "confidence": validation.response.confidence,
                "reasoning": validation.response.reasoning,
            }
        ),
        metadata_mapper=lambda validation: {
            "planner": "llm",
            "model": MODEL_PROFILES.get(ModelProfile.PLANNER).model_id,
            "prompt_version": "v1",
            "valid": validation.valid,
        },
    )
    async def plan(
        self,
        state: AdvisorState,
    ) -> PlannerValidationResult:

        request = self._prompt_builder.build(state)

        response = await self._llm_gateway.generate(
            request=request,
            model_profile=ModelProfile.PLANNER,
        )
        try:
            planner = self._parser.parse(response.answer)
        except PlannerParserError as ex:
            return PlannerValidationResult(
            valid=False,
            response=None,
            errors=[
                PlannerError(
                    field="response",
                    message=str(ex),
                )
            ],
        )

        return self._validator.validate(planner)