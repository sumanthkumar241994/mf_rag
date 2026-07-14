from dataclasses import dataclass

from app.dtos.llm.llm_response import LLMResponse


@dataclass(slots=True)
class LLMChunk:
    token: str | None = None
    response: LLMResponse | None = None