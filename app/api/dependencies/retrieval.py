from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends
from app.api.dependencies.database import get_db
from app.business.document.services.context_builder import ContextBuilder
from app.business.document.services.retrieval_service import RetrievalService
from app.repositories import DocumentChunkRepository
from app.llm_gateway.embeddings.bedrock_embedding_client import  BedrockEmbeddingClient
from app.core.config.aws import AWS

async def get_retrieval_service(db: AsyncSession = Depends(get_db)) -> RetrievalService:
    chunk_repository = DocumentChunkRepository(db=db)
    embedding_client = BedrockEmbeddingClient(AWS().bedrock_runtime)
    return RetrievalService(embedding_client=embedding_client, chunk_repository=chunk_repository)


def get_context_builder() -> ContextBuilder:
    return ContextBuilder()
