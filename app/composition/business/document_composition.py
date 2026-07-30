from sqlalchemy.ext.asyncio import AsyncSession
from app.business.advisor.enums.capabilities import Capability
from app.business.advisor.enums.tool_type import ToolType
from app.business.document.document_service import DocumentService
from app.business.document.services.context_builder import ContextBuilder
from app.business.document.services.retrieval_service import RetrievalService
from app.composition.database_composition import DatabaseComposition
from app.llm_gateway.embeddings.bedrock_titan_embedding import BedrockTitanEmbedding
from app.repositories.chunk_repository import DocumentChunkRepository
from app.services.document_chunk_service import DocumentChunkService
from app.tools.definitions.tool_definition import ToolDefinition
from app.tools.implementations.document_tool import DocumentTool
from app.workflows.workflow.service.workflow_service import WorkflowService
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

class DocumentComposition:
    def __init__(
        self,
        database: DatabaseComposition,
        workflow_service: WorkflowService,
    ):
        self.context_builder = ContextBuilder()
        self.document_chunk_service = DocumentChunkService(
            session_factory=database.session_factory,
        )
        self.retrieval_service = RetrievalService(
            embedding_client=BedrockTitanEmbedding(),
            document_chunk_service=self.document_chunk_service
        )
        
        self.workflow_service = workflow_service

        self.document_service = DocumentService(
            retrieval_service=self.retrieval_service,
            context_builder=self.context_builder,
            workflow_service=workflow_service
        )

        self.definition = ToolDefinition(
            name=ToolType.DOCUMENT_SEARCH.value,
            description=(
                "Search mutual fund documents to retrieve relevant information "
                "and supporting context for answering customer queries."
            ),
            capability=Capability.DOCUMENT,
            timeout_seconds=30,
            tags=[
                "document",
                "search",
                "retrieval",
                "mutual-fund",
                "scheme",
                "sid",
                "kim",
                "factsheet",
                "annual-report",
                "exit-load",
                "expense-ratio",
                "investment-objective",
                "fund-manager",
                "risk",
                "nav",
            ],
        )

        self.tool = DocumentTool(
            document_service=self.document_service,
        )

