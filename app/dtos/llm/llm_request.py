from dataclasses import dataclass

from app.dtos.llm.llm_response_format import ResponseFormat

@dataclass(slots=True)
class LLMRequest:
    user_prompt: str
    system_prompt: str
    temperature: float = 0.0
    max_tokens: int = 2000
    response_format: ResponseFormat | None = None