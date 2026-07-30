# app/agents/base_agent.py

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, AsyncIterator

from app.dtos.agents.agent_response import AgentResponse
from app.dtos.agents.stream_event import AgentStreamEvent
from app.dtos.request_context import RequestContext


class BaseAgent(ABC):
    """
    Base contract for all agents.

    Responsible for:
    - Creating workflow state
    - Executing workflow
    - Resuming workflow
    - Streaming workflow execution
    """

    @property
    @abstractmethod
    def workflow_name(self) -> str:
        """
        Name used for conversation persistence.
        Example:
            advisor
            investment
        """
        raise NotImplementedError

    @abstractmethod
    def create_state(
        self,
        request: RequestContext,
        history: list[Any],
        trace_id: str,
    ) -> Any:
        """
        Creates the workflow state required by the agent.
        """
        raise NotImplementedError

    @abstractmethod
    async def run(
        self,
        state: Any,
    ) -> AgentResponse:
        """
        Execute the workflow.
        """
        raise NotImplementedError

    @abstractmethod
    async def resume(
        self,
        state: Any,
    ) -> AgentResponse:
        """
        Resume an interrupted workflow.
        """
        raise NotImplementedError

    @abstractmethod
    async def stream(
        self,
        state: Any,
    ) -> AsyncIterator[AgentStreamEvent]:
        """
        Stream workflow execution.
        """
        raise NotImplementedError

    @abstractmethod
    async def resume_stream(
        self,
        state: Any,
    ) -> AsyncIterator[AgentStreamEvent]:
        """
        Resume and stream an interrupted workflow.
        """
        raise NotImplementedError