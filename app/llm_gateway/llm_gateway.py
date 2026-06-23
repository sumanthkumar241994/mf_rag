from app.dtos.llm.llm_request import LLMRequest
from app.dtos.llm.llm_response import LLMResponse

from app.llm_gateway.providers.base import LLMProvider

class LLMGateway:
    def __init__(self, provider: LLMProvider):
        self.provider = provider
    
    async def generate(self, request: LLMRequest) -> LLMResponse:
        return await self.provider.generate(request)
