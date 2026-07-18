
from app.ai.guardrails.llm.llm_guard_parser import LLMGuardParser
from app.ai.guardrails.llm.llm_guard_prompt_builder import LLMGuardPromptBuilder
from app.ai.guardrails.llm.llm_validator import LLMGuardValidator
from app.ai.guardrails.llm.models.llm_guard_response import LLMGuardResponse
from app.dtos.llm.llm_request import LLMRequest

from app.dtos.request_context import RequestContext
from app.llm_gateway.enums.model_profile import ModelProfile
from app.llm_gateway.llm_gateway import LLMGateway


class LLMGuardService:

    def __init__(
        self,
        prompt_builder: LLMGuardPromptBuilder,
        llm_gateway: LLMGateway,
        parser: LLMGuardParser,
        validator: LLMGuardValidator,
    ):
        self._prompt_builder = prompt_builder
        self._llm_gateway = llm_gateway
        self._parser = parser
        self._validator = validator

    async def validate(
        self,
        request_context: RequestContext,
    ) -> LLMGuardResponse:
        try:
            request: LLMRequest = self._prompt_builder.build(
                query=request_context.query,
            )

            llm_response = await self._llm_gateway.generate(
                request=request,
                model_profile=ModelProfile.GUARDRAIL,
            )

            response = self._parser.parse(
                llm_response.answer,
            )

            validation = self._validator.validate(
                response,
            )

            if not validation.valid:
                raise ValueError("; ".join(validation.errors))

            return validation.response
        
        except Exception as ex:
            return LLMGuardResponse(
                allowed=False,
                confidence=0.0,
                reason="Unable to validate the request.",
            )