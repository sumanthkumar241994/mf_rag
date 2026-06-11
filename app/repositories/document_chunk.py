from sqlalchemy.orm import Session
from app.models import DocumentChunk

class DocumentChunkRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, chunk: DocumentChunk):
        self.db.add(chunk)
        self.db.flush()
        return chunk

    def get_by_hash(self, chunk_hash: str):
        return (
            self.db.query(DocumentChunk)
            .filter(
                DocumentChunk.chunk_hash == chunk_hash
            )
            .first()
        )
