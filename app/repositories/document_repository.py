from uuid import UUID

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.models.document import Document
from app.repositories.base_repository import BaseRepository


class DocumentRepository(BaseRepository):
    def __init__(self, db: AsyncSession):
        super().__init__(db)

    async def get_by_id(self, document_id: UUID) -> Document | None:
        stmt = select(Document).where(Document.id == document_id)
        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def get_by_scheme_code(self, scheme_code: str) -> list[Document]:
        stmt = select(Document).where(Document.scheme_code == scheme_code)
        result = await self.db.execute(stmt)

        return result.scalars().all()

    async def create(self, document: Document) -> Document:
        await self.db.add(document)
        await self.db.flush()
        await self.db.refresh(document)
        
        return document
    
    async def list_documents(self, limit: int = 100, offset: int = 0) -> list[Document]:
        stmt = select(Document).offset(offset).limit(limit).order_by(Document.created_at.desc())
        result = await self.db.execute(stmt)

        return result.scalar().all()

    async def delete(self, document_id: UUID) -> None:
        document = self.get_by_id(document_id=document_id)

        if document:
            await self.db.delete(document)



    



