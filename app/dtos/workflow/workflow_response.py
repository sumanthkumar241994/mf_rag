from dataclasses import dataclass, field
from typing import Any

from app.business.document.models.retrieval_response import SourceResponse
from app.dtos.llm.llm_metrics import LLMMetrics
from app.dtos.llm.llm_usage import LLMUsage

@dataclass(slots=True)
class WorkflowResponse:
    answer: str
    sources: list[SourceResponse]
    retrieved_chunks: int
    llm_usage: LLMUsage | None = None
    llm_metrics: LLMMetrics | None = None
    metadata: dict[str, Any] = field(default_factory=dict)