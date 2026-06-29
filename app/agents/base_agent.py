from __future__ import annotations

from abc import ABC, abstractmethod
from typing import AsyncIterator

from app.dtos.agents.agent_request import AgentRequest
from app.dtos.agents.agent_response import AgentResponse
from app.enums.workflow import WorkflowType

class BaseAgent(ABC):

    workflow: WorkflowType

    @abstractmethod
    async def run(self, request: AgentRequest) -> AgentResponse:
        raise NotImplementedError

    @abstractmethod
    async def stream(self, request: AgentRequest) -> AgentResponse:
        raise NotImplementedError
    
    
