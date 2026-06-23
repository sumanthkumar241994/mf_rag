from fastapi import Depends
from app.advisor.advisor_service import AdvisorService
from app.api.dependencies.retrieval import get_retrieval_service
from app.llm_gateway import llm_gateway
from app.llm_gateway.providers.bedrock_gemma_gateway import GemmaProvider
from app.retrieval.context_builder import ContextBuilder
from app.llm_gateway.llm_gateway import LLMGateway


async def get_advisor_service(retrieval_service=Depends(get_retrieval_service)) -> AdvisorService:
    context_builder = ContextBuilder()
    llm_gateway = LLMGateway(GemmaProvider())

    return AdvisorService(
        context_builder=context_builder,
        retrieval_service=retrieval_service,
        llm_gateway=llm_gateway
    )