from dataclasses import dataclass
from app.dtos.llm.llm_usage import LLMUsage
from app.dtos.llm.llm_metrics import LLMMetrics

@dataclass(slots=True)
class LLMStreamResponse:
    answer: str = ""
    usage: LLMUsage | None = None
    metrics: LLMMetrics | None = None

    def to_dict(self) -> dict:
        payload = {
            "answer": self.answer,
        }

        if self.usage:
            payload["usage"] = self.usage.to_dict()

        if self.metrics:
            payload["metrics"] = self.metrics.to_dict()

        return payload