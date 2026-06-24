# app/api/dependencies/tool.py

from fastapi import Depends

from app.retrieval.retrieval_service import RetrievalService

from app.tools.registry.tool_registry import ToolRegistry
from app.tools.executor.tool_executor import ToolExecutor

from app.tools.definitions.tool_definition import ToolDefinition
from app.tools.implementations.document_search_tool import DocumentSearchTool

from app.api.dependencies.retrieval import get_retrieval_service


def get_tool_registry(retrieval_service: RetrievalService = Depends(get_retrieval_service)) -> ToolRegistry:
    registry = ToolRegistry()

    registry.register(
        ToolDefinition(
            name='document_search',
            description='Search mutual fund documents using semantic search',
            category='retrieval',
            timeout_seconds=10,
            allowed_agents=['advisor'],
            tags = ["rag","documents", "mutual-funds"]
        ),
        DocumentSearchTool(retrieval_service=retrieval_service)
    )

    return registry


def get_tool_executor(registry: ToolRegistry = Depends(get_tool_registry)) -> ToolExecutor:
    return ToolExecutor(tool_registry=registry)
