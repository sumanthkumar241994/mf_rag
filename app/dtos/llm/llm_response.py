from dataclasses import dataclass

@dataclass(slots=True)
class LLMResponse:
    answer: str
    model: str
    input_tokens: int | None = None
    output_tokens: int | None = None