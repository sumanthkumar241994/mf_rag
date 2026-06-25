from typing import AsyncIterator
from abc import ABC, abstractmethod
from app.dtos.llm.llm_request import LLMRequest
from app.dtos.llm.llm_response import LLMResponse

class LLMProvider(ABC):

    @abstractmethod
    async def generate(
        self,
        request: LLMRequest
    ) -> LLMResponse:
        pass

    @abstractmethod
    async def stream(
        self,
        request: LLMRequest
    ) -> AsyncIterator[str]:
        pass