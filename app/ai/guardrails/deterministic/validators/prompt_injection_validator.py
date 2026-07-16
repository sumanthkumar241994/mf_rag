from app.ai.guardrails.deterministic.models.guardrail_result import GuardRailResult
from app.ai.guardrails.deterministic.validators.base import GuardRailValidator
from app.dtos.request_context import RequestContext


class PromptInjectionValidator(GuardRailValidator):
    """
    Detects common prompt injection attempts.

    This validator blocks obvious attacks only.
    More sophisticated attacks can later be handled
    using an LLM-based validator.
    """

    BLOCKED_PATTERNS = (
        "ignore previous instructions",
        "ignore all previous instructions",
        "forget previous instructions",
        "forget all instructions",
        "reveal system prompt",
        "show system prompt",
        "print system prompt",
        "display system prompt",
        "developer message",
        "hidden prompt",
        "internal prompt",
        "you are chatgpt",
        "act as",
        "pretend to be",
        "jailbreak",
        "bypass",
        "override instructions",
        "disable guardrails",
        "system prompt",
    )

    async def validate(
        self,
        request_context: RequestContext,
    ) -> GuardRailResult:

        query = request_context.query.lower()

        for pattern in self.BLOCKED_PATTERNS:

            if pattern in query:

                return GuardRailResult(
                    allowed=False,
                    reason="PROMPT_INJECTION",
                    response=(
                        "I can't process requests that attempt to modify "
                        "or bypass my operating instructions."
                    ),
                )

        return GuardRailResult(allowed=True)