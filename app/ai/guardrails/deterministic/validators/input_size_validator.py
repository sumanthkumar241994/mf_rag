

from app.ai.guardrails.deterministic.models.guardrail_result import GuardRailResult
from app.ai.guardrails.deterministic.validators.base import GuardRailValidator
from app.dtos.request_context import RequestContext


class InputSizeValidator(GuardRailValidator):
    """
    Validates the incoming user query size.

    Prevents:
    - Empty requests
    - Extremely long prompts
    - Prompt stuffing attacks
    """

    MAX_QUERY_LENGTH = 5000

    async def validate(
        self,
        request_context: RequestContext,
    ) -> GuardRailResult:

        query = request_context.query.strip()

        if not query:
            return GuardRailResult(
                allowed=False,
                reason="EMPTY_QUERY",
                response="Please enter a question related to mutual funds or investments.",
            )

        if len(query) > self.MAX_QUERY_LENGTH:
            return GuardRailResult(
                allowed=False,
                reason="QUERY_TOO_LARGE",
                response=(
                    f"Your request exceeds the maximum supported length of "
                    f"{self.MAX_QUERY_LENGTH} characters. "
                    "Please shorten your query and try again."
                ),
            )

        return GuardRailResult(
            allowed=True,
        )