
from app.ai.guardrails.llm.models.llm_guard_response import LLMGuardResponse
from app.ai.guardrails.llm.models.llm_guard_validation_result import LLMGuardValidationResult


class LLMGuardValidator:
    """
    Validates the parsed LLM Guard response.
    """

    MIN_CONFIDENCE = 0.70

    def validate(
        self,
        response: LLMGuardResponse,
    ) -> LLMGuardValidationResult:

        errors: list[str] = []

        if not isinstance(response.allowed, bool):
            errors.append("'allowed' must be a boolean.")

        if not 0.0 <= response.confidence <= 1.0:
            errors.append("'confidence' must be between 0.0 and 1.0.")

        if not response.reason.strip():
            errors.append("'reason' cannot be empty.")

        if errors:
            return LLMGuardValidationResult(
                valid=False,
                response=None,
                errors=errors,
            )

        # Low confidence responses are treated as invalid.
        if response.confidence < self.MIN_CONFIDENCE:
            return LLMGuardValidationResult(
                valid=False,
                response=response,
                errors=[
                    f"Guard confidence {response.confidence:.2f} is below "
                    f"the minimum threshold {self.MIN_CONFIDENCE:.2f}."
                ],
            )

        return LLMGuardValidationResult(
            valid=True,
            response=response,
            errors=[],
        )