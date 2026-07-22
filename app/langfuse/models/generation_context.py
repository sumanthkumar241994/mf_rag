from dataclasses import dataclass
from typing import Any


@dataclass(slots=True)
class GenerationContext:
    model: str

    system_prompt: str | None
    user_prompt: str | None

    response: str | None

    finish_reason: str | None

    input_tokens: int
    output_tokens: int
    total_tokens: int

    latency_ms: int | None
    first_token_latency_ms: int | None

    total_cost: float | None

    metadata: dict[str, Any]