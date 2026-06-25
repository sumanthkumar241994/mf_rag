# app/llm_gateway/streaming/llm_stream_collector.py

from dataclasses import dataclass, field
from dtos.llm.llm_metrics import LLMMetrics
from dtos.llm.llm_usage import LLMUsage


@dataclass(slots=True)
class LLMStreamCollector:
    """
    Collects the streamed LLM tokens and metadata
    """
    tokens: list[str] = field(default_factory=list)
    usage: LLMUsage | None = None
    metrics: LLMMetrics | None = None

    def add_token(self, token: str):
        self.tokens.append(token)
    
    @property
    def answer(self) -> str:
        return "".join(self.tokens)