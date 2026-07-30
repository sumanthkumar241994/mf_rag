

from app.agents.planner.agent_planner import AgentPlanner
from app.business.advisor.enums.agent_type import AgentType
from app.dtos.agents.agent_plan import AgentPlan
from app.dtos.agents.agent_request import AgentRequest


class RuleBasedAgentPlanner(AgentPlanner):

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
    }

    INVESTMENT_KEYWORDS = {
        "invest",
        "buy",
        "purchase",
        "redeem",
        "redemption",
        "switch",
        "sip",
        "stp",
        "swp",
        "withdraw",
        "sell",
        "cancel sip",
        "stop sip",
    }

    async def plan(
        self,
        request: AgentRequest,
    ) -> AgentPlan:

        query = request.request.query.lower()

        advisor = self._contains(query, self.ADVISOR_KEYWORDS)
        investment = self._contains(query, self.INVESTMENT_KEYWORDS)

        agents: list[AgentType] = []

        if advisor:
            agents.append(AgentType.ADVISOR)

        if investment:
            agents.append(AgentType.INVESTMENT)

        if not agents:
            # Default informational queries to Advisor
            agents.append(AgentType.ADVISOR)

        return AgentPlan(
            agents=agents,
            reason=self._reason(advisor, investment),
        )

    @staticmethod
    def _contains(
        query: str,
        keywords: set[str],
    ) -> bool:
        return any(keyword in query for keyword in keywords)

    @staticmethod
    def _reason(
        advisor: bool,
        investment: bool,
    ) -> str:

        if advisor and investment:
            return "Request spans multiple business capabilities."

        if advisor:
            return "Advisory request."

        if investment:
            return "Investment execution request."

        return "Defaulted to advisor."