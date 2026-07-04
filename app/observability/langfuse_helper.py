# app/observability/langfuse_helper.py

from langfuse import get_client

from app.dtos.llm.llm_request import LLMRequest
from app.dtos.llm.llm_metrics import LLMMetrics
from app.dtos.llm.llm_usage import LLMUsage

langfuse = get_client()

# version for streaming later thought of having same code for both generate and streaming
# def update_generation(request: LLMRequest, collector: StreamCollector):
#     langfuse.update_current_generation(
#         input={
#             "system_prompt": request.system_prompt,
#             "user_prompt": request.user_prompt,
#         },
#         output=collector.answer,
#         model=collector.model,
#         usage_details={
#             "input": collector.input_tokens,
#             "output": collector.output_tokens
#         },
#         metadata={
#             "latency_ms": collector.latency_ms,
#             "cost": collector.cost,
#             "finish_reason": collector.finish_reason
#         }

#     )

def get_trace_id() -> str | None:
    return langfuse.get_current_trace_id()


def get_observation_id() -> str | None:
    return langfuse.get_current_observation_id()


def update_generation(request: LLMRequest, answer: str, usage: LLMUsage, metrics: LLMMetrics) -> None:
    langfuse.update_current_generation(
        input = {
            "system_prompt": request.system_prompt,
            "user_prompt": request.user_prompt,
            "context": request.context
        },
        output=answer,
        model=metrics.model,
        usage_details={
            "input": usage.input_tokens,
            "output": usage.output_tokens
        },
        metadata={
            "latency_ms": metrics.latency_ms,
            "first_token_latency_ms": metrics.first_token_latency_ms,
            "invocation_latency_ms": metrics.invocation_latency_ms,
            "gateway_overhead_ms": metrics.gateway_overhead_ms,
            "cost": metrics.cost,
            "finish_reason": metrics.finish_reason
        }
    )

