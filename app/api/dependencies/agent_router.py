from app.agents.planner.rule_based_agent_classifier import RuleBasedAgentClassifier
from app.agents.router.agent_router import AgentRouter

_agentrouter: AgentRouter | None = None

def get_agent_router() -> AgentRouter:
    global _agentrouter

    if _agentrouter is None:
        return AgentRouter(RuleBasedAgentClassifier())
    
    return _agentrouter
