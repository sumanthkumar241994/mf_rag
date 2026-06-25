# app/dtos/llm/llm_usage.py
from dataclasses import dataclass

@dataclass(slots=True)
class LLMUsage:
    input_tokens: int | None = None
    output_tokens: int | None = None
    total_tokens: int | None = None