from app.dtos.llm.llm_request import LLMRequest

from app.prompts.system.advisor_system_prompt import ADVISOR_SYSTEM_PROMPT
from app.retrieval.retrieval_service import RetrievalService
from app.retrieval.context_builder import ContextBuilder
from app.llm_gateway.llm_gateway import LLMGateway
from app.schemas.responses.advisor import AdvisorResponse, SourceResponse

from app.observability.tracing import trace_workflow

class AdvisorService:
    def __init__(
        self,
        retrieval_service: RetrievalService,
        context_builder: ContextBuilder,
        llm_gateway: LLMGateway
    ):
        self.retrieval_service = retrieval_service
        self.context_builder = context_builder
        self.llm_gateway = llm_gateway
    
    @trace_workflow("advisor_chat")
    async def chat(
        self,
        query: str
    ) -> AdvisorResponse:
        chunks = await self.retrieval_service.retrieve(
            query=query,
            top_k=10,
        )

        llm_context = self.context_builder.build(chunks)

        response = await self.llm_gateway.generate(
            LLMRequest(
                user_prompt=query,
                system_prompt=ADVISOR_SYSTEM_PROMPT,
                context=llm_context.context
            )
        )
        
        return AdvisorResponse(
            answer=response.answer,
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
        )
