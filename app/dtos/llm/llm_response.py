from dataclasses import asdict, dataclass
from typing import Any
from app.dtos.llm.llm_usage import LLMUsage
from app.dtos.llm.llm_metrics import LLMMetrics

@dataclass(slots=True)
class LLMResponse:
    answer: str
    structured_output: Any | None = None
    usage: LLMUsage | None = None
    metrics: LLMMetrics | None = None

    def to_dict(self) -> dict:
        payload = {
            "answer": self.answer,
        }

        if self.structured_output is not None:
            if hasattr(self.structured_output, "model_dump"):          # Pydantic v2
                payload["structured_output"] = self.structured_output.model_dump()
            elif hasattr(self.structured_output, "dict"):             # Pydantic v1
                payload["structured_output"] = self.structured_output.dict()
            else:
                payload["structured_output"] = asdict(self.structured_output)

        if self.usage:
            payload["usage"] = self.usage.to_dict()

        if self.metrics:
            payload["metrics"] = self.metrics.to_dict()

        return payload