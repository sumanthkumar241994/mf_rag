#           Version 1
#  from fastapi import Depends
# from app.services.advisor_service import AdvisorService
# from app.api.dependencies.retrieval import get_retrieval_service
# from app.llm_gateway import llm_gateway
# from app.llm_gateway.providers.bedrock_gemma_gateway import GemmaProvider
# from app.retrieval.context_builder import ContextBuilder
# from app.llm_gateway.llm_gateway import LLMGateway


# async def get_advisor_service(retrieval_service=Depends(get_retrieval_service)) -> AdvisorService:
#     context_builder = ContextBuilder()
#     llm_gateway = LLMGateway(GemmaProvider())

#     return AdvisorService(
#         context_builder=context_builder,
#         retrieval_service=retrieval_service,
#         llm_gateway=llm_gateway
#     )

from fastapi import Depends
from app.services.advisor_service import AdvisorService
from app.agents.advisor_agent import AdvisorAgent
from app.api.dependencies.agent import get_advisor_agent
from app.api.dependencies.orchestrator import get_orchestrator
from app.orchestration.orchestrator import Orchestrator



async def get_advisor_service(
    advisor_agent: AdvisorAgent=Depends(get_advisor_agent), 
    orchestrator: Orchestrator=Depends(get_orchestrator)
) -> AdvisorService:

    return AdvisorService(
        advisor_agent=advisor_agent,
        orchestrator=orchestrator
    )