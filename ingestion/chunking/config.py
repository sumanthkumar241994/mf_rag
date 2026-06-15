from dataclasses import dataclass

@dataclass(frozen=True)
class ChunkingConfig:
    target_tokens: int = 700
    overlap_tokens: int = 100
    min_chunk_tokens: int = 50