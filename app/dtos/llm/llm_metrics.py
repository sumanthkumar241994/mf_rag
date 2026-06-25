# app/dtos/llm/llm_metrics.py

from dataclasses import dataclass

@dataclass(slots=True)
class LLMMetrics:
    model: str
    latency_ms: int
    first_token_latency_ms: int | None = None
    invocation_latency_ms: int | None = None
    gateway_overhead_ms: int | None = None
    cost: float = 0.0
    finish_reason: str | None = None
