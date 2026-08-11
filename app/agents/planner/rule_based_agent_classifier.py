from app.agents.planner.agent_classifier import AgentClassifier
from app.business.advisor.enums.agent_type import AgentType
from app.dtos.agents.agent_plan import AgentPlan
from app.dtos.agents.agent_request import AgentRequest
from app.enums.workflow import WorkflowType


class RuleBasedAgentClassifier(AgentClassifier):

    ADVISOR_KEYWORDS = {
        "compare",
        "comparison",
        "recommend",
        "recommendation",
        "suggest",
        "analysis",
        "analyze",
        "review",
        "returns",
        "return",
        "performance",
        "risk",
        "portfolio",
        "explain",
        "difference",
        "better",
        "best",
        "eligible",
        "eligibility",
        "onboarding",
        "onboarding status",
        "kyc status",
        "kyc",
        "registration",
        "registered",
        "account status",
    }

    PURCHASE_KEYWORDS = {
        "buy",
        "purchase",
        "place order",
        "place an order",
        "make a purchase",
        "invest in",
        "invest ₹",
        "invest rs",
        "invest rs.",
        "invest ",
        "start sip",
        "start an sip",
    }

    REDEMPTION_KEYWORDS = {
        "redeem",
        "redemption",
        "withdraw",
        "sell",
    }

    SWITCH_KEYWORDS = {
        "switch",
    }

    STP_KEYWORDS = {
        "stp",
    }

    SWP_KEYWORDS = {
        "swp",
        "cancel sip",
        "stop sip",
    }

    async def classify(
        self,
        request: AgentRequest,
    ) -> AgentPlan:

        query = request.request.query.lower()

        workflow = self._workflow(query)

        primary_agent = (
            AgentType.INVESTMENT
            if workflow is not None
            else AgentType.ADVISOR
        )

        return AgentPlan(
            primary_agent=primary_agent,
            workflow=workflow,
            confidence=1.0,
            reason=self._reason(query, workflow),
            metadata={
                "classifier": "rule_based",
                "workflow": (
                    workflow.value
                    if workflow
                    else None
                ),
            },
        )

    def _workflow(
        self,
        query: str,
    ) -> WorkflowType | None:

        if self._is_purchase_request(query):
            return WorkflowType.INVESTMENT_PURCHASE

        if self._contains(query, self.REDEMPTION_KEYWORDS):
            return WorkflowType.INVESTMENT_REDEMPTION

        if self._contains(query, self.SWITCH_KEYWORDS):
            return WorkflowType.INVESTMENT_SWITCH

        if self._contains(query, self.STP_KEYWORDS):
            return WorkflowType.INVESTMENT_STP

        if self._contains(query, self.SWP_KEYWORDS):
            return WorkflowType.INVESTMENT_SWP

        return None

    @staticmethod
    def _contains(
        query: str,
        keywords: set[str],
    ) -> bool:
        return any(
            keyword in query
            for keyword in keywords
        )

    @staticmethod
    def _reason(
        query: str,
        workflow: WorkflowType | None,
    ) -> str:

        if workflow is not None:
            return (
                f"Investment {workflow.value} request."
            )

        return "Advisory request."

    def _is_purchase_request(
    self,
    query: str,
    ) -> bool:

        if self._contains(
            query,
            {
                "buy",
                "purchase",
                "place order",
                "place an order",
                "make a purchase",
                "start sip",
                "start an sip",
            },
        ):
            return True

        # "invest <amount> in <scheme>"
        if (
            query.startswith("invest ")
            and " in " in query
        ):
            return True

        return False