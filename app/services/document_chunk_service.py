from contextlib import asynccontextmanager

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
)

from app.repositories.chunk_repository import DocumentChunkRepository


class DocumentChunkService:

    def __init__(
        self,
        session_factory: async_sessionmaker[AsyncSession],
    ):
        self._session_factory = session_factory

    @asynccontextmanager
    async def repository(self):
        async with self._session_factory() as session:
            yield DocumentChunkRepository(session)

    async def similarity_search(
        self,
        embedding: list[float],
        top_k: int,
        scheme_name: str | None = None,
        document_type: str | None = None,
    ):
        async with self.repository() as repository:
            return await repository.similarity_search(
                embedding=embedding,
                top_k=top_k,
                scheme_name=scheme_name,
                document_type=document_type,
            )