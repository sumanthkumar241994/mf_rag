from dataclasses import asdict
from app.business.advisor.models.planner_result import PlannerResult
from app.business.advisor.planner.exceptions import PlannerParserError
from app.business.advisor.planner.models.planner_error import PlannerError
from app.business.advisor.planner.models.planner_validation_result import (
    PlannerValidationResult,
)
from app.business.advisor.planner.planner_parser import PlannerParser
from app.business.advisor.planner.planner_validator import PlannerValidator
from app.business.advisor.planner.tool_mapper import ToolMapper
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
        tool_mapper: ToolMapper
    ):
        self._prompt_builder = prompt_builder
        self._llm_gateway = llm_gateway
        self._parser = parser
        self._validator = validator
        self._tool_mapper = tool_mapper

    @trace_step(
        "llm_planner",
        input_mapper=lambda self, state: {
            "query": state.request.query,
        },
        output_mapper=lambda result: {
            "intent": result.intent.value,
            "capabilities": [
                {
                    "capability": c.capability.value,
                    "confidence": c.confidence,
                }
                for c in result.capabilities
            ],
            "selected_tools": [
                tool.value
                for tool in result.selected_tools
            ],
            "confidence": result.confidence,
            "reasoning": result.reasoning,
        },
        metadata_mapper=lambda result: {
            "planner": "llm",
            "model": MODEL_PROFILES[
                ModelProfile.PLANNER
            ].model_id,
            "prompt_version": "v1",
        },
    )
    async def plan(
        self,
        state: AdvisorState,
    ) -> PlannerResult:

        request = self._prompt_builder.build(state)
        try:
            response = await self._llm_gateway.generate(
                request=request,
                model_profile=ModelProfile.PLANNER,
            )

            planner_response = self._parser.parse(response.answer)
            validation = self._validator.validate(planner_response)

            if not validation.valid:
                raise PlannerError(
                    "; ".join(
                        error.message
                        for error in validation.errors
                    )
                )

            selected_tools = self._tool_mapper.map(
                planner_response.capability_matches
            )

            return PlannerResult(
                intent=planner_response.intent,
                capabilities=planner_response.capability_matches,
                selected_tools=selected_tools,
                confidence=planner_response.confidence,
                reasoning=planner_response.reasoning,
            )

        except PlannerError:
            raise

        except Exception as ex:
            raise PlannerError(
                "Planner execution failed."
            ) from ex
        