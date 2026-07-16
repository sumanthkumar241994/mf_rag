

from app.ai.guardrails.deterministic.models.guardrail_result import GuardRailResult
from app.ai.guardrails.deterministic.validators.base import GuardRailValidator
from app.dtos.request_context import RequestContext


class DomainValidator(GuardRailValidator):
    """
    Validates whether the query belongs to the Mutual Fund Advisor domain.

    This validator is intentionally conservative.
    More advanced semantic validation will be handled
    later by an LLM-based validator.
    """

    DOMAIN_KEYWORDS = {
        "mutual fund",
        "fund",
        "portfolio",
        "sip",
        "systematic investment plan",
        "lumpsum",
        "stp",
        "swp",
        "scheme",
        "nav",
        "elss",
        "etf",
        "equity",
        "debt",
        "hybrid",
        "index fund",
        "large cap",
        "mid cap",
        "small cap",
        "flexi cap",
        "tax",
        "capital gains",
        "redemption",
        "switch",
        "goal",
        "retirement",
        "wealth",
        "investment",
        "invest",
        "risk",
        "kyc",
        "nominee",
        "onboarding",
    }

    async def validate(
        self,
        request_context: RequestContext,
    ) -> GuardRailResult:

        query = request_context.query.lower()

        if any(keyword in query for keyword in self.DOMAIN_KEYWORDS):
            return GuardRailResult(allowed=True)

        return GuardRailResult(
            allowed=False,
            reason="OUT_OF_DOMAIN",
            response=(
                "I'm designed to help with mutual funds, investments, SIPs, "
                "portfolios, taxation, onboarding, and related financial topics."
            ),
        )