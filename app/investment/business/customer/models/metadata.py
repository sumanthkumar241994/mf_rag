from dataclasses import dataclass
from datetime import datetime


@dataclass(slots=True)
class KnowledgeMetadata:
    source: str | None
    updated_at: datetime | None
    confidence: float | None