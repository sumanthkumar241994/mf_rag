from dataclasses import replace
import json
from typing import AsyncIterator
from app.dtos.agents.stream_event import AgentStreamEvent
from app.dtos.llm.llm_chunk import LLMChunk
from app.dtos.llm.llm_request import LLMRequest
from app.dtos.llm.llm_response import LLMResponse
from app.dtos.llm.llm_response_format import ResponseFormat
from app.dtos.llm.llm_stream_response import LLMStreamResponse

from app.llm_gateway.enums.model_profile import ModelProfile
from app.llm_gateway.enums.provider import Provider
from app.llm_gateway.model_profiles import MODEL_PROFILES
import app.observability.langfuse_helper as LangfuseHelper

from app.enums.stream_event_type import StreamEventType
from app.events.models.llm_generation_completed_event import LLMGenerationCompletedEvent
from app.llm_gateway.providers.base import LLMProvider

from app.events.publishers.sqs_publisher import SQSEventPublisher

from app.llm_gateway.metrics.cost_calculator import CostCalculator

import logging 

logger = logging.getLogger(__name__)

class LLMGateway:
    def __init__(
        self, 
        providers: dict[Provider,LLMProvider], 
        sqs_publisher: SQSEventPublisher
    ):
        self.providers = providers
        self.sqs_publisher = sqs_publisher
    
    async def generate(self, request: LLMRequest, model_profile: ModelProfile = ModelProfile.CHAT, trace: bool=True) -> LLMResponse:
        model_config = MODEL_PROFILES[model_profile]
        provider = self.providers[model_config.provider]
        request = self._prepare_request(request, provider)
        response = await provider.generate(request, model_id=model_config.model_id)

        if request.response_model:
            try:
                response.structured_output = (
                    request.response_model.model_validate_json(
                        response.answer
                    )
                )
            except Exception as ex:
                logger.exception(
                    f"Failed to parse structured response: {str(ex)}"
                )
                raise ValueError(
                    f"Unable to parse response as "
                    f"{request.response_model.__name__}"
                ) from ex

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
        if trace:
            await self.sqs_publisher.publish(
                LLMGenerationCompletedEvent(
                    trace_id=LangfuseHelper.get_trace_id(),
                    parent_observation_id=LangfuseHelper.get_observation_id(),
                    request=request,
                    answer=response.answer,
                    usage=response.usage,
                    metrics=response.metrics
                )
            )

        return response

    # async def stream(self, request: LLMRequest) -> AsyncIterator[AgentStreamEvent]:
    #     async for event in self.provider.stream(request):
    #         if event.type == StreamEventType.COMPLETED.value and event.response:
    #             event.response.metrics.cost = CostCalculator.calculate(
    #                             model=event.response.metrics.model,
    #                             input_tokens=event.response.usage.input_tokens,
    #                             output_tokens=event.response.usage.output_tokens
    #                         )

    #             await self.sqs_publisher.publish(
    #                     LLMGenerationCompletedEvent(
    #                         trace_id=LangfuseHelper.get_trace_id(),
    #                         parent_observation_id=LangfuseHelper.get_observation_id(),
    #                         request=request,
    #                         answer=event.response.answer,
    #                         usage=event.response.usage,
    #                         metrics=event.response.metrics
    #                     )
    #                 )

    #         yield event

    async def astream(
        self, 
        request: LLMRequest, 
        model_profile: ModelProfile= ModelProfile.CHAT
    ) -> AsyncIterator[LLMChunk]:

        model_config = MODEL_PROFILES[model_profile]
        provider = self.providers[model_config.provider]
        async for chunk in provider.astream(request, model_id=model_config.model_id):
            if chunk.response is not None:
                response = chunk.response

                if response.metrics is not None and response.usage is not None:
                    response.metrics.cost = CostCalculator.calculate(
                                model=response.metrics.model,
                                input_tokens=response.usage.input_tokens,
                                output_tokens=response.usage.output_tokens
                            )

                    await self.sqs_publisher.publish(
                        LLMGenerationCompletedEvent(
                            trace_id=LangfuseHelper.get_trace_id(),
                            parent_observation_id=LangfuseHelper.get_observation_id(),
                            request=request,
                            answer=response.answer,
                            usage=response.usage,
                            metrics=response.metrics
                        )
                    )

                
            yield chunk
        
    def _prepare_request(
    self,
    request: LLMRequest,
    provider: LLMProvider,
    ) -> LLMRequest:

        if request.response_model is None:
            return request

        # Later:
        # if provider.supports_native_structured_output:
        #     return request

        schema = request.response_model.model_json_schema()

        system_prompt = (
            request.system_prompt
            + "\n\n"
            + self._structured_output_instruction(schema)
        )

        return replace(
            request,
            system_prompt=system_prompt,
        )
        

    import json


    @staticmethod
    def _structured_output_instruction(
        schema: dict,
    ) -> str:

        return f"""
# Structured Output Requirements

Return ONLY a valid JSON object.

Requirements:

- The response MUST be valid JSON.
- The response MUST conform to the JSON schema below.
- Do NOT wrap the JSON in markdown.
- Do NOT include explanations before or after the JSON.
- Do NOT include fields that are not defined in the schema.
- All required fields must be present.

JSON Schema:

{json.dumps(schema, indent=2)}
""".strip()
        
        

        
        
