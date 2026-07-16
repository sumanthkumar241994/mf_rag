from dataclasses import dataclass

from app.ai.guardrails.llm.models.llm_guard_response import LLMGuardResponse


@dataclass(slots=True)
class LLMGuardValidationResult:
    valid: bool
    response: LLMGuardResponse | None
    errors: list[str]