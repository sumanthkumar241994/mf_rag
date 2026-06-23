from dataclasses import dataclass

@dataclass(slots=True)
class LLMRequest:
    query: str
    system_prompt: str
    user_prompt: str | None = None
    context: str | None = None
    temperature: float = 0.0
    max_tokens: int = 2000