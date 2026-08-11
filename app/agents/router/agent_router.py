from app.agents.planner.agent_classifier import AgentClassifier
from app.dtos.agents.agent_plan import AgentPlan
from app.dtos.agents.agent_request import AgentRequest


class AgentRouter:

    def __init__(
        self,
        classifier: AgentClassifier,
    ):
        self._classifier = classifier

    async def route(
        self,
        request: AgentRequest,
    ) -> AgentPlan:
        return await self._classifier.classify(request)