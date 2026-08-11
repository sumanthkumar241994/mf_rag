from abc import ABC, abstractmethod

from app.dtos.agents.agent_plan import AgentPlan
from app.dtos.agents.agent_request import AgentRequest



class AgentClassifier(ABC):

    @abstractmethod
    async def classify(
        self,
        request: AgentRequest,
    ) -> AgentPlan:
        """
        Determine which business capabilities (agents)
        are required to satisfy the request.
        """
        raise NotImplementedError