
from app.api.dependencies.advisor_agent import get_advisor_agent
from app.api.dependencies.agent_router import get_agent_router
from app.api.dependencies.conversation import get_conversation_service
from app.api.dependencies.investment_agent import get_investment_agent
from app.composition.guardrail_composition import GuardRailComposition
from app.composition.llm_composition.gemma_composition import LLMComposition
from app.orchestration.orchestrator import Orchestrator


_orchestrator: Orchestrator | None = None

def get_orchestrator(
) -> Orchestrator:
    global _orchestrator

    if _orchestrator is None:
        llm = LLMComposition()
        guardrails = GuardRailComposition(
            llm_gateway=llm.gateway,
        )
        return Orchestrator(
            conversation_service=get_conversation_service(),
            advisor_agent=get_advisor_agent(),
            investment_agent=get_investment_agent(),
            agent_router=get_agent_router(),
            guardrail_service=guardrails.guardrail_service
            )

    return _orchestrator