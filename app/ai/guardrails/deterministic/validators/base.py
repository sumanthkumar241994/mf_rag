from abc import ABC, abstractmethod

from app.ai.guardrails.deterministic.models.guardrail_result import GuardRailResult
from app.dtos.request_context import RequestContext



class GuardRailValidator(ABC):

    @abstractmethod
    async def validate(
        self,
        request: RequestContext,
    ) -> GuardRailResult:
        pass