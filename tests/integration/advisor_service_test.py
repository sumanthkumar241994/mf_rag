import asyncio
from app.dtos.llm.llm_request import LLMRequest
from app.llm_gateway.router import LLMRouter
from app.llm_gateway.llm_gateway import LLMGateway
from app.retrieval.context_builder import ContextBuilder
from app.prompts.system.advisor_system_prompt import ADVISOR_SYSTEM_PROMPT
from app.api.dependencies.database import AsyncSessionLocal
from app.repositories import DocumentChunkRepository
from app.retrieval.retrieval_service import RetrievalService
from app.llm_gateway.embeddings.bedrock_embedding_client import  BedrockEmbeddingClient
from app.core.config.aws import AWS


async def test_rag_to_claude():
    async with AsyncSessionLocal() as db:
        chunk_repository = DocumentChunkRepository(db=db)
        embedding_client = BedrockEmbeddingClient(AWS().bedrock_runtime)

        retrieval_service = RetrievalService(embedding_client, chunk_repository)
        chunks = await retrieval_service.retrieve(query='What are the risk factors?', top_k=5)

        print(f"Retrived {len(chunks)} chunks")
        llm_context = ContextBuilder().build(chunks)

        provider = LLMRouter.get_provider()
        gateway = LLMGateway(provider=provider)

        response = await gateway.generate(
                LLMRequest(
                    user_prompt='What are the risk factors?',
                    context=llm_context.context,
                    system_prompt=ADVISOR_SYSTEM_PROMPT
                )
            )

        print(response.answer)


if __name__ == '__main__':
    asyncio.run(test_rag_to_claude())
