from dataclasses import dataclass

@dataclass(slots=True)
class LLMRequest:
    user_prompt: str
    system_prompt: str
    temperature: float = 0.0
    max_tokens: int = 2000