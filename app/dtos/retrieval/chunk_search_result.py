from dataclasses import dataclass
from app.models import Document, DocumentChunk, DocumentVersion, VersionChunkMapping

@dataclass(slots=True)
class ChunkSearchResult:
    document: Document
    chunk: DocumentChunk
    version: DocumentVersion
    mapping: VersionChunkMapping
    distance: float
