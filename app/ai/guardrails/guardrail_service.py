from app.ai.guardrails.deterministic.models.guardrail_result import GuardRailResult
from app.ai.guardrails.deterministic.validators.base import GuardRailValidator
from app.ai.guardrails.llm.llm_guard_service import LLMGuardService
from app.dtos.request_context import RequestContext

class GuardRailService:
    """
    Executes all configured guard rail validators.

    Validation stops on the first failure.
    """

    def __init__(
        self,
        validators: list[GuardRailValidator],
        llm_guard_service: LLMGuardService | None = None,
    ):
        self._validators = validators
        self._llm_guard_service = llm_guard_service

    async def validate(
        self,
        request_context: RequestContext,
    ) -> GuardRailResult:

        # Stage 1
        for validator in self._validators:

            result = await validator.validate(request_context)

            if not result.allowed:
                return result

        # Stage 2
        # if self._llm_guard_service:

        #     llm_result = await self._llm_guard_service.validate(
        #         request_context,
        #     )

        #     if not llm_result.allowed:
        #         return GuardRailResult(
        #             allowed=False,
        #             reason="LLM_GUARD_REJECTED",
        #             response=llm_result.reason,
        #         )

        return GuardRailResult(
            allowed=True,
        )