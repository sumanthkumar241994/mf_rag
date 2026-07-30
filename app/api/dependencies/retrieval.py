# from sqlalchemy.ext.asyncio import AsyncSession
# from fastapi import Depends
# from app.api.dependencies.database import get_db
# from app.business.document.services.context_builder import ContextBuilder
# from app.business.document.services.retrieval_service import RetrievalService
# from app.llm_gateway.embeddings.bedrock_titan_embedding import BedrockTitanEmbedding
# from app.repositories import DocumentChunkRepository
# from app.core.config.aws import AWS

# async def retrieval_service(db: AsyncSession = Depends(get_db)) -> RetrievalService:
#     chunk_repository = DocumentChunkRepository(db=db)
#     embedding_client = BedrockTitanEmbedding()
#     return RetrievalService(embedding_client=embedding_client, chunk_repository=chunk_repository)

# def get_retrieval_service():
#     return retrieval_service()

# def get_context_builder() -> ContextBuilder:
#     return ContextBuilder()
