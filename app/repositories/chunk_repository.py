from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.business.document.models.chunk_search_result import ChunkSearchResult
from app.models import Document, DocumentChunk, DocumentVersion, VersionChunkMapping
from app.repositories.base_repository import BaseRepository



class DocumentChunkRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_by_id(self, chunk_id: UUID) -> DocumentChunk | None:
        stmt = select(DocumentChunk).where(DocumentChunk.id == chunk_id)
        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_chunk_hash(self, chunk_hash: str) -> DocumentChunk | None:
        stmt = select(DocumentChunk).where(DocumentChunk.chunk_hash == chunk_hash)
        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def create(self, chunk: DocumentChunk) -> DocumentChunk:
        await self.db.add(chunk)
        await self.db.flush()
        await self.db.refresh(chunk)

        return chunk
    
    async def list_chunks(self, limit: int = 100, offset: int = 0) -> list[DocumentChunk]:
        stmt = select(DocumentChunk).offset(offset).limit(limit).order_by(DocumentChunk.created_at.desc())
        result = await self.db.execute(stmt)

        return result.scalars().all()

    async def delete(self, chunk_id: UUID) -> None:
        chunk = await self.get_by_id(chunk_id=chunk_id)

        if chunk:
            await self.db.delete(chunk)
    
    async def similarity_search(
        self,  
        embedding: list[float], 
        top_k: int = 10, 
        scheme_name: str | None = None, 
        document_type: str | None = None
    ):
        distance = DocumentChunk.embedding.cosine_distance(embedding).label("distance")
        stmt = (
                select(
                    DocumentChunk,
                    VersionChunkMapping,
                    DocumentVersion,
                    Document,
                    distance
                )
                .join(
                    VersionChunkMapping,
                    VersionChunkMapping.chunk_id == DocumentChunk.id

                )
                .join(
                    DocumentVersion,
                    DocumentVersion.id == VersionChunkMapping.document_version_id
                )
                .join(
                    Document,
                    Document.id == DocumentVersion.document_id
                )
                .where(
                    DocumentVersion.is_active.is_(True)
                )
            )  
        
        if scheme_name:
            stmt = stmt.where(Document.scheme_name == scheme_name)
        
        if document_type:
            stmt = stmt.where(Document.document_type == document_type)

        stmt = stmt.order_by(distance).limit(top_k)
        
        result = await self.db.execute(stmt)

        rows = result.all()
        return [ChunkSearchResult(chunk=chunk, mapping=mapping,version=version, document=document,distance=distance) for (chunk,mapping,version,document,distance) in rows]



