from abc import ABC, abstractmethod

from app.dtos.agents.agent_plan import AgentPlan
from app.dtos.agents.agent_request import AgentRequest



class AgentPlanner(ABC):

    @abstractmethod
    async def plan(
        self,
        request: AgentRequest,
    ) -> AgentPlan:
        """
        Determine which business capabilities (agents)
        are required to satisfy the request.
        """
        raise NotImplementedError