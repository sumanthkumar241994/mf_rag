from dataclasses import dataclass, field
from typing import Any


@dataclass(slots=True)
class RetrievedChunk:
    chunk_id: str | None
    document_id: str | None
    document_name: str | None

    content: str

    score: float | None

    metadata: dict[str, Any] = field(default_factory=dict)

@dataclass(slots=True)
class RetrievalContext:
    tool: str | None

    query: str | None

    chunks: list[RetrievedChunk] = field(default_factory=list)

    chunk_count: int = 0

    truncated: bool = False
