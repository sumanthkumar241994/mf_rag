from app.ai.guardrails.deterministic.models.guardrail_result import GuardRailResult
from app.ai.guardrails.deterministic.validators.base import GuardRailValidator
from app.dtos.request_context import RequestContext


class AbuseValidator(GuardRailValidator):
    """
    Detects abusive or malicious requests.

    This validator blocks obvious misuse attempts.
    It is intentionally conservative and can be
    extended over time.
    """

    BLOCKED_PATTERNS = (
        "hack",
        "hacking",
        "exploit",
        "exploit this",
        "sql injection",
        "drop table",
        "delete database",
        "ddos",
        "phishing",
        "malware",
        "ransomware",
        "virus",
        "steal",
        "steal password",
        "bypass authentication",
        "bypass login",
        "credential stuffing",
        "brute force",
        "fraud",
        "money laundering",
        "terrorist",
        "bomb",
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
                    reason="ABUSIVE_REQUEST",
                    response=(
                        "I'm unable to assist with requests involving illegal, "
                        "malicious, or abusive activities."
                    ),
                )

        return GuardRailResult(
            allowed=True,
        )