from app.business.advisor.enums.capabilities import Capability
from app.business.advisor.models.advisor_error import AdvisorError
from app.business.common.services.base_workflow_service import BaseWorkflowService
from app.business.document.models.document_context import DocumentContext
from app.business.document.models.retrieval_response import SourceResponse
from app.business.document.services.context_builder import ContextBuilder
from app.business.document.services.retrieval_service import RetrievalService
from app.observability.tracing import trace_step
from app.workflows.advisor.advisor_state import AdvisorState
from app.workflows.workflow.models.workflow_execution import WorkflowExecution
from app.workflows.workflow.service.workflow_service import WorkflowService


class DocumentService(BaseWorkflowService[DocumentContext]):

    def __init__(
        self,
        retrieval_service: RetrievalService,
        context_builder: ContextBuilder,
        workflow_service: WorkflowService,
    ):
        super().__init__(workflow_service)
        self._retrieval_service = retrieval_service
        self._context_builder = context_builder


    @trace_step(
        "document_search_tool",
        output_mapper=lambda execution: (
            {"success": False}
            if execution is None
            else {
                "success": True,
                "chunks": execution.result.chunk_count,
                "truncated": execution.result.truncated,
            }
        ),
        metadata_mapper=lambda result: {
            "tool": "document_search",
        },
)
    async def retrieve(
        self,
        state: AdvisorState,
    ) -> WorkflowExecution[DocumentContext] | None:
        """
        Retrieves relevant document chunks and builds
        the LLM-ready context.

        The resulting context and sources are stored in AdvisorState.
        """

        try:
            chunks = await self._retrieval_service.retrieve(
                query=state.request.query,
            )

        except Exception as ex:
            state.workflow_execution = None
            state.add_error(
                AdvisorError.from_exception(
                    error=ex,
                    source="document_retrieval",
                )
            )
            return None

        llm_context = self._context_builder.build(chunks)

        sources = [
            SourceResponse(
                source_id=source_id,
                scheme_name=chunk.scheme_name,
                document_type=chunk.document_type,
                section_name=chunk.section_name,
                page_no=chunk.page_no,
            )
            for source_id, chunk in llm_context.source_map.items()
        ]

        document_context = DocumentContext(
            llm_context=llm_context,
            sources=sources,
        )

        execution = self._create_workflow_execution(
            state=state,
            capability=Capability.DOCUMENT,
            result=document_context,
            complete=True,
        )

        state.llm_context = document_context.llm_context
        state.sources = document_context.sources
        state.workflow_execution = execution

        return execution