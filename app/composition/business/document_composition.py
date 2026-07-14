from app.business.advisor.enums.capabilities import Capability
from app.business.advisor.enums.tool_type import ToolType
from app.business.document.document_service import DocumentService
from app.business.document.services.context_builder import ContextBuilder
from app.business.document.services.retrieval_service import RetrievalService
from app.tools.definitions.tool_definition import ToolDefinition
from app.tools.implementations.document_tool import DocumentTool
from app.workflows.workflow.service.workflow_service import WorkflowService


class DocumentComposition:
    def __init__(
        self,
        retrieval_service: RetrievalService,
        workflow_service: WorkflowService,
        context_builder: ContextBuilder
    ):
        self.retrieval_service = retrieval_service
        self.context_builder = context_builder
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

