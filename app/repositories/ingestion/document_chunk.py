from sqlalchemy.orm import Session
from app.models import DocumentChunk

class DocumentChunkRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(
        self,
        *,
        chunk_hash: str,
        content: str,
        token_count: int,
        embedding_model: str,
        embedding: list[float],
    ) -> DocumentChunk:

        chunk = DocumentChunk(
            chunk_hash=chunk_hash,
            content=content,
            token_count=token_count,
            embedding_model=embedding_model,
            embedding=embedding,
        )

        self.db.add(chunk)
        self.db.flush()

        return chunk

    def find_by_hash(self, chunk_hash: str):
        return (
            self.db.query(DocumentChunk)
            .filter(
                DocumentChunk.chunk_hash == chunk_hash
            )
            .first()
        )
