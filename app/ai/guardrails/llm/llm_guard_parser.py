import json

from app.ai.guardrails.llm.exceptions import LLMGuardParserError
from app.ai.guardrails.llm.models.llm_guard_response import LLMGuardResponse



class LLMGuardParser:

    def parse(
        self,
        response: str,
    ) -> LLMGuardResponse:

        try:
            payload = json.loads(response)
        except json.JSONDecodeError as exc:
            raise LLMGuardParserError(
                "Invalid JSON returned by LLM Guard."
            ) from exc

        try:
            allowed = payload["allowed"]
        except KeyError as exc:
            raise LLMGuardParserError(
                "LLM Guard response missing 'allowed'."
            ) from exc

        if not isinstance(allowed, bool):
            raise LLMGuardParserError(
                "'allowed' must be a boolean."
            )

        try:
            confidence = float(payload["confidence"])
        except KeyError as exc:
            raise LLMGuardParserError(
                "LLM Guard response missing 'confidence'."
            ) from exc
        except (TypeError, ValueError) as exc:
            raise LLMGuardParserError(
                "'confidence' must be a float."
            ) from exc

        try:
            reason = payload["reason"].strip()
        except KeyError as exc:
            raise LLMGuardParserError(
                "LLM Guard response missing 'reason'."
            ) from exc
        except AttributeError as exc:
            raise LLMGuardParserError(
                "'reason' must be a string."
            ) from exc

        return LLMGuardResponse(
            allowed=allowed,
            confidence=confidence,
            reason=reason,
        )