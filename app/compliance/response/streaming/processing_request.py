from dataclasses import dataclass, replace

from app.business.advisor.enums.intent import Intent
from app.business.document.models.llm_context import LLMContext


@dataclass(slots=True, frozen=True)
class ProcessingRequest:
    text: str
    intent: Intent | None = None
    context: LLMContext | None = None

    def with_text(
        self,
        text: str,
    ) -> "ProcessingRequest":
        return replace(
            self,
            text=text,
        )