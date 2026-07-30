from app.business.document.models.retrieved_chunk import RetrievedChunk
from app.llm_gateway.embeddings.bedrock_titan_embedding import BedrockTitanEmbedding
from app.observability.tracing import trace_step
from app.services.document_chunk_service import DocumentChunkService


class RetrievalService:
    def __init__(
        self,
        embedding_client: BedrockTitanEmbedding,
        document_chunk_service: DocumentChunkService,
    ):
        self.embedding_client = embedding_client
        self.document_chunk_service = document_chunk_service

    @trace_step("retrieve_documents")
    async def retrieve(
        self,
        query: str,
        top_k: int = 5,
        scheme_name: str | None = None,
        document_type: str | None = None,
    ) -> list[RetrievedChunk]:

        # Generate query embedding
        query_embedding = await self.embedding_client.generate(query)

        # Vector search
        results = await self.document_chunk_service.similarity_search(
            embedding=query_embedding,
            top_k=top_k,
            scheme_name=scheme_name,
            document_type=document_type,
        )

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
                    distance=result.distance,
                )
            )

        return retrieved_chunks