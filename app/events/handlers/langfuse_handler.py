# app/events/handlers/langfuse_handler.py

from langfuse import Langfuse

from app.events.handlers.base import EventHandler
from app.events.models.llm_generation_completed_event import LLMGenerationCompletedEvent

import logging
logger = logging.getLogger(__name__)

class LangfuseHandler(EventHandler[LLMGenerationCompletedEvent]):
    """
    Publishes complete LLM generations to Langfuse
    """
    critical = True
    def __init__(self, langfuse: Langfuse):
        self.langfuse = langfuse

    async def handle(self, event: LLMGenerationCompletedEvent):
        trace_context = {}
        print(f"Langfuse event: {event}")
        if event.trace_id:
            trace_context['trace_id'] = event.trace_id
        
        if event.parent_observation_id:
            trace_context["parent_span_id"] = event.parent_observation_id

        trace_context = trace_context or None
        
        try:
            with self.langfuse.start_as_current_observation(
                as_type='generation',
                name='bedrock-generation',
                trace_context=trace_context,
                model=event.metrics.model,
                input = {
                    "system_prompt": event.request.system_prompt,
                    "user_prompt": event.request.user_prompt,
                },
                output=event.answer,
                usage_details={
                    "input": event.usage.input_tokens,
                    "output": event.usage.output_tokens
                },
                metadata={
                    "event_id": event.event_id,
                    "correlation_id": event.correlation_id,
                    "latency_ms": event.metrics.latency_ms,
                    "first_token_latency_ms": event.metrics.first_token_latency_ms,
                    "invocation_latency_ms": event.metrics.invocation_latency_ms,
                    "gateway_overhead_ms": event.metrics.gateway_overhead_ms,
                    "cost": event.metrics.cost,
                    "finish_reason": event.metrics.finish_reason
                }

            ) as generation:
                print(f"Generation: {generation}")
        except Exception as ex:
            print(f"failed to publish the generation to langfuse: {str(ex)}")