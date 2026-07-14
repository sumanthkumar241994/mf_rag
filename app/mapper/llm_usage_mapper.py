from app.dtos.llm.llm_usage import LLMUsage


class LLMUsageMapper:

    @staticmethod
    def from_dict(
        data: dict | LLMUsage | None,
    ) -> LLMUsage | None:

        if data is None:
            return None

        if isinstance(data, LLMUsage):
            return data

        return LLMUsage(
            input_tokens=data.get("prompt_tokens", 0),
            output_tokens=data.get("completion_tokens", 0),
            total_tokens=data.get("total_tokens", 0),
        )