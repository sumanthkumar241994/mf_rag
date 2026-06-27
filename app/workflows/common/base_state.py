from typing import NotRequired, TypedDict

from app.dtos.llm.llm_metrics import LLMMetrics
from app.dtos.llm.llm_usage import LLMUsage
from app.schemas.conversation.cache_message import CacheMessage


class BaseWorkflowState(TypedDict):
    query: str
    history: list[CacheMessage]

    llm_usage: NotRequired[LLMUsage]
    llm_metrics: NotRequired[LLMMetrics]