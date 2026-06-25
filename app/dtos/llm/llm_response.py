from dataclasses import dataclass
from app.dtos.llm.llm_usage import LLMUsage
from app.dtos.llm.llm_metrics import LLMMetrics

@dataclass(slots=True)
class LLMResponse:
    answer: str
    usage: LLMUsage | None = None
    metrics: LLMMetrics | None = None