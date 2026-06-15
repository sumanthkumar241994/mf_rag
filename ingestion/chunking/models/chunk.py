from dataclasses import dataclass
from .chunk_metadata import ChunkMetadata

@dataclass(slots=True)
class Chunk:
    content: str
    token_count: int
    metadata: ChunkMetadata
    