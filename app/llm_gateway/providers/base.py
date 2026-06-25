from typing import AsyncIterator
from abc import ABC, abstractmethod
from app.dtos.llm.llm_request import LLMRequest
from app.dtos.llm.llm_response import LLMResponse
from app.dtos.llm.llm_stream_response import LLMStreamResponse

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
        request: LLMRequest,
        stream_response: LLMStreamResponse
    ) -> AsyncIterator[str]:
        pass