from app.dtos.llm.llm_metrics import LLMMetrics


class LLMMetricsMapper:

    @staticmethod
    def from_dict(
        data: dict | LLMMetrics | None,
    ) -> LLMMetrics | None:

        if data is None:
            return None

        if isinstance(data, LLMMetrics):
            return data

        return LLMMetrics(
            model=data.get("model"),
            latency_ms=data.get("latency_ms"),
            first_token_latency_ms=data.get(
                "first_token_latency_ms"
            ),
            invocation_latency_ms=data.get(
                "invocation_latency_ms"
            ),
            gateway_overhead_ms=data.get(
                "gateway_overhead_ms"
            ),
            cost=data.get("cost", 0.0),
            finish_reason=data.get("finish_reason"),
        )