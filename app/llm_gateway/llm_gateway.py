from typing import AsyncIterator
from app.dtos.llm.llm_request import LLMRequest
from app.dtos.llm.llm_response import LLMResponse

from app.llm_gateway.providers.base import LLMProvider

from app.llm_gateway.metrics.cost_calculator import CostCalculator
from app.observability.langfuse_helper import update_generation

class LLMGateway:
    def __init__(self, provider: LLMProvider):
        self.provider = provider
    
    async def generate(self, request: LLMRequest) -> LLMResponse:
        response = await self.provider.generate(request)

        response.metrics.cost = CostCalculator.calculate(
            model=response.metrics.model,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens
        )

        update_generation(
            request=request,
            answer=response.answer,
            usage=response.usage,
            metrics=response.metrics
        )

        return response
        
    async def stream(self, request: LLMRequest) -> AsyncIterator[str]:
        async for chunk in self.provider.stream(request):
            yield chunk