from app.ai.guardrails.deterministic.models.guardrail_result import GuardRailResult
from app.ai.guardrails.deterministic.validators.base import GuardRailValidator
from app.ai.guardrails.enums import GuardRailCategory
from app.dtos.request_context import RequestContext


import json
from collections.abc import Mapping, Sequence


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

        texts: list[str] = []

        #
        # Initial user query
        #
        if request_context.query:
            texts.append(request_context.query)

        #
        # Workflow resume
        #
        if request_context.workflow_resume is not None:
            texts.extend(
                self._extract_strings(
                    request_context.workflow_resume,
                )
            )

        for text in texts:
            lowered = text.lower()

            for pattern in self.BLOCKED_PATTERNS:
                if pattern in lowered:
                    return GuardRailResult(
                        allowed=False,
                        reason="PROMPT_INJECTION",
                        category=GuardRailCategory.PROMPT_INJECTION.value,
                        response=(
                            "I can't process requests that attempt to modify "
                            "or bypass my operating instructions."
                        ),
                    )

        return GuardRailResult(
            allowed=True,
        )

    def _extract_strings(
        self,
        value,
    ) -> list[str]:

        if value is None:
            return []

        if isinstance(value, str):
            return [value]

        if isinstance(value, Mapping):
            result: list[str] = []
            for v in value.values():
                result.extend(
                    self._extract_strings(v)
                )
            return result

        if (
            isinstance(value, Sequence)
            and not isinstance(value, (str, bytes))
        ):
            result: list[str] = []
            for item in value:
                result.extend(
                    self._extract_strings(item)
                )
            return result

        return []