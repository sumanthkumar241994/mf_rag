from app.models import document
from app.repositories import DocumentRepository, DocumentChunkRepository
from app.schemas.responses.retrieval import RetrievedChunk
from app.llm_gateway.embeddings.bedrock_embedding_client import BedrockEmbeddingClient

from app.observability.tracing import trace_step


class RetrievalService:
    def __init__(
        self,
        embedding_client: BedrockEmbeddingClient,
        chunk_repository: DocumentChunkRepository
    ):
        self.embedding_client = embedding_client
        self.chunk_repository = chunk_repository

    @trace_step("retrieve_documents")
    async def retrieve(
        self,
        query: str,
        top_k: int = 10,
        scheme_name: str | None = None,
        document_type: str | None = None
    ) -> list[RetrievedChunk]:
        # Generate query embedding
        query_embedding = await self.embedding_client.generate(query)

        #vector search
        results = (
            await self.chunk_repository.similarity_search(
                embedding=query_embedding,
                top_k=top_k,
                scheme_name=scheme_name,
                document_type=document_type
            )
        )

        # Transform into response DTO
        retrieved_chunks = []

        for result in results:
            retrieved_chunks.append(
                RetrievedChunk(
                    chunk_id=result.chunk.id,
                    content=result.chunk.content,
                    scheme_name=result.document.scheme_name,
                    amc_name=result.document.amc_name,
                    document_type=result.document.document_type,
                    section_name=result.mapping.section_name,
                    page_no=result.mapping.page_no,
                    distance=result.distance
                )
            )

        return retrieved_chunks