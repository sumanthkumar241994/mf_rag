from dataclasses import dataclass


@dataclass(slots=True)
class LLMUsage:
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None

@dataclass(slots=True)
class LLMResponse:
    answer: str
    model: str
    usage: LLMUsage | None = None
    latency_ms: int | None = None