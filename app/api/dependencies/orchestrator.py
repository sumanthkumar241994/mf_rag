
from app.agents.planner.rule_based_agent_planner import RuleBasedAgentPlanner
from app.api.dependencies.advisor_agent import get_advisor_agent
from app.api.dependencies.agent_planner import get_rule_based_agent_palnner
from app.api.dependencies.conversation import get_conversation_service
from app.api.dependencies.investment_agent import get_investment_agent
from app.orchestration.orchestrator import Orchestrator


_orchestrator: Orchestrator | None = None

def get_orchestrator(
) -> Orchestrator:
    global _orchestrator

    if _orchestrator is None:
        return Orchestrator(
            conversation_service=get_conversation_service(),
            advisor_agent=get_advisor_agent(),
            investment_agent=get_investment_agent(),
            planner=get_rule_based_agent_palnner()
            )

    return _orchestrator