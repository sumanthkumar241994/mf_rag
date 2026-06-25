from typing import AsyncIterator
from app.dtos.llm.llm_request import LLMRequest
from app.dtos.llm.llm_response import LLMResponse
from app.dtos.llm.llm_stream_response import LLMStreamResponse

from langfuse import get_client

from app.events.models.llm_generation_completed_event import LLMGenerationCompletedEvent
from app.llm_gateway.providers.base import LLMProvider

from app.events.publishers.sqs_publisher import SQSEventPublisher

from app.llm_gateway.metrics.cost_calculator import CostCalculator

class LLMGateway:
    def __init__(self, provider: LLMProvider, sqs_publisher: SQSEventPublisher):
        self.provider = provider
        self.sqs_publisher = sqs_publisher
    
    async def generate(self, request: LLMRequest) -> LLMResponse:
        response = await self.provider.generate(request)

        response.metrics.cost = CostCalculator.calculate(
            model=response.metrics.model,
            input_tokens=response.usage.input_tokens,
            output_tokens=response.usage.output_tokens
        )

        # update_generation(
        #     request=request,
        #     answer=response.answer,
        #     usage=response.usage,
        #     metrics=response.metrics
        # )
        langfuse = get_client()
        
        trace_id = langfuse.get_current_trace_id()
        parent_observation_id = langfuse.get_current_observation_id()

        await self.sqs_publisher.publish(
            LLMGenerationCompletedEvent(
                trace_id=trace_id,
                parent_observation_id=parent_observation_id,
                request=request,
                answer=response.answer,
                usage=response.usage,
                metrics=response.metrics
            )
        )

        return response

    async def stream(self, request: LLMRequest) -> AsyncIterator[str]:
        stream_repsonse = LLMStreamResponse()
        async for chunk in self.provider.stream(request, stream_repsonse):
            yield chunk
        
        stream_repsonse.metrics.cost = CostCalculator.calculate(
            model=stream_repsonse.metrics.model,
            input_tokens=stream_repsonse.usage.input_tokens,
            output_tokens=stream_repsonse.usage.output_tokens
        )

        langfuse = get_client()
        
        trace_id = langfuse.get_current_trace_id()
        parent_observation_id = langfuse.get_current_observation_id()

        await self.sqs_publisher.publish(
            LLMGenerationCompletedEvent(
                trace_id=trace_id,
                parent_observation_id=parent_observation_id,
                request=request,
                answer=stream_repsonse.answer,
                usage=stream_repsonse.usage,
                metrics=stream_repsonse.metrics
            )
        )
        
