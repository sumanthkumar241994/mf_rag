from app.dtos.llm.llm_response import LLMResponse
from app.mapper.llm_metrics_mapper import LLMMetricsMapper
from app.mapper.llm_usage_mapper import LLMUsageMapper


class LLMResponseMapper:

    @staticmethod
    def from_dict(data: dict | LLMResponse | None) -> LLMResponse | None:

        if data is None:
            return None

        if isinstance(data, LLMResponse):
            return data

        return LLMResponse(
            answer=data.get("answer", ""),
            usage=LLMUsageMapper.from_dict(
                data.get("usage")
            ),
            metrics=LLMMetricsMapper.from_dict(
                data.get("metrics"),
            ),
        )