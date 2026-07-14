from dataclasses import dataclass

from app.business.document.models.llm_context import LLMContext
from app.business.document.models.retrieval_response import SourceResponse


@dataclass
class DocumentContext:
    llm_context: LLMContext
    sources: list[SourceResponse]