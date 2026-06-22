from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.schema import DropColumnComment

from app.models.document_chunk import DocumentChunk
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
