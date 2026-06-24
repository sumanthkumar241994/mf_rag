# app/workflows/nodes/build_context_node.py

from app.workflows.advisor.advisor_state import AdvisorState
from app.retrieval.context_builder import ContextBuilder
from app.schemas.responses.advisor import SourceResponse
from app.observability.tracing import trace_step

class BuildContextNode:
    def __init__(
        self,
        context_builder: ContextBuilder
    ):
        self.context_builder = context_builder
    
    @trace_step("build_context")
    async def __call__(
        self,
        state: AdvisorState
    ) -> dict:
        llm_context = self.context_builder.build(state['chunks'])

        sources = [
            SourceResponse(
                source_id=source_id,
                scheme_name=chunk.scheme_name,
                document_type=chunk.document_type,
                section_name=chunk.section_name,
                page_no=chunk.page_no
            )
            for source_id, chunk in llm_context.source_map.items()
        ]

        return {
            "context": llm_context.context,
            "sources": sources
        }

