from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.api.dependencies.database import get_db
from app.repositories import DocumentChunkRepository
from app.services import RetrievalService, BedrockEmbeddingService
from app.core.config.aws import AWS

async def get_retrieval_service(db: AsyncSession = Depends(get_db)) -> RetrievalService:
    chunk_repository = DocumentChunkRepository(db=db)
    embedding_service = BedrockEmbeddingService(AWS().bedrock_runtime)
    return RetrievalService(embedding_service=embedding_service, chunk_repository=chunk_repository)
