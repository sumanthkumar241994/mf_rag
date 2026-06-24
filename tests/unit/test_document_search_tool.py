import asyncio

from app.core.database import AsyncSessionLocal
from app.core.config.aws import AWS

from app.repositories import DocumentChunkRepository
from app.retrieval.retrieval_service import RetrievalService
from app.llm_gateway.embeddings.bedrock_embedding_client import (
    BedrockEmbeddingClient,
)

from app.tools.registry.tool_registry import ToolRegistry
from app.tools.executor.tool_executor import ToolExecutor
from app.tools.definitions.tool_definition import ToolDefinition
from app.tools.implementations.document_search_tool import (
    DocumentSearchTool,
)


async def test_document_search_tool():

    async with AsyncSessionLocal() as db:

        retrieval_service = RetrievalService(
            embedding_client=BedrockEmbeddingClient(
                AWS().bedrock_runtime
            ),
            chunk_repository=DocumentChunkRepository(
                db=db
            ),
        )

        registry = ToolRegistry()

        registry.register(
            ToolDefinition(
                name="document_search",
                description="Search mutual fund documents",
                category="retrieval",
            ),
            DocumentSearchTool(
                retrieval_service=retrieval_service
            ),
        )

        executor = ToolExecutor(
            tool_registry=registry
        )

        response = await executor.execute(
            tool_name="document_search",
            arguments={
                "query": "What are the risk factors?",
            },
        )

        print("Success:", response.success)
        print("Execution Time:", response.execution_time_ms)

        if response.success:
            print("Chunks:", len(response.result))

            for chunk in response.result[:3]:
                print(chunk.scheme_name)
                print(chunk.content[:200])
                print("-" * 50)
        else:
            print(response.error)


if __name__ == "__main__":
    asyncio.run(
        test_document_search_tool()
    )