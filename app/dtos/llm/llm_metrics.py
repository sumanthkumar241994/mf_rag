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

    def to_dict(self) -> dict:
        payload = {
            "model": self.model,
        }

        if self.latency_ms is not None:
            payload["latency_ms"] = self.latency_ms

        if self.first_token_latency_ms is not None:
            payload["first_token_latency_ms"] = self.first_token_latency_ms

        if self.invocation_latency_ms is not None:
            payload["invocation_latency_ms"] = self.invocation_latency_ms

        if self.gateway_overhead_ms is not None:
            payload["gateway_overhead_ms"] = self.gateway_overhead_ms

        if self.cost is not None:
            payload["cost"] = self.cost

        if self.finish_reason is not None:
            payload["finish_reason"] = self.finish_reason

        return payload