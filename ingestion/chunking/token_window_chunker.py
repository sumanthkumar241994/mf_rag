from pydantic.type_adapter import R
from sqlalchemy import over
from ingestion.chunking.config import ChunkingConfig

class TokenWindowChunker:

    def __init__(self, config: ChunkingConfig) -> None:
        self.config = config

    def split(self, text: str) -> list[str]:
        words = text.split()

        if not words:
            return []
        
        target = self.config.target_tokens
        overlap = self.config.overlap_tokens

        chunks = []

        start = 0

        while start < len(words):
            end = min(start+target, len(words))

            chunk_words = words[start: end]
            chunks.append(" ".join(chunk_words))

            if end == len(words):
                break
            
            start = end - overlap
        return chunks

        