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
from app.agents.advisor_agent import AdvisorAgent
from app.api.dependencies.customer import get_customer_gateway
from app.api.dependencies.portfolio import get_portfolio_gateway
from app.api.dependencies.scheme import get_scheme_gateway
from app.business.customer.gateway.customer_gateway import CustomerGateway
from app.business.portfolio.gateways.portfolio_gateway import PortfolioGateway
from app.business.scheme.gateways.scheme_gateway import SchemeGateway
from app.composition.advisor_composition import AdvisorComposition
from app.composition.business.customer_composition import CustomerComposition
from app.composition.business.portfolio_composition import PortfolioComposition
from app.composition.business.scheme_composition import SchemeComposition
from app.composition.llm_composition.gemma_composition import LLMComposition
from app.composition.planner.hybrid_planner_composition import HybridPlannerComposition
from app.composition.prompt.advisor_prompt_composition import AdvisorPromptComposition
from app.composition.tool_composition import ToolComposition
from app.services.advisor_service import AdvisorService
from app.api.dependencies.orchestrator import get_orchestrator
from app.orchestration.orchestrator import Orchestrator

_advisor : AdvisorComposition | None = None

def get_advisor_agent(
    portfolio_gateway: PortfolioGateway = Depends(get_portfolio_gateway),
    scheme_gateway: SchemeGateway = Depends(get_scheme_gateway),
    customer_gateway: CustomerGateway = Depends(get_customer_gateway)
) -> AdvisorAgent:
    global _advisor
    if _advisor is None:
        portfolio = PortfolioComposition(portfolio_gateway=portfolio_gateway)
        scheme = SchemeComposition(scheme_gateway=scheme_gateway)
        customer = CustomerComposition(customer_gateway=customer_gateway),
        tools = ToolComposition()
        prompt = AdvisorPromptComposition()
        llm = LLMComposition()
        planner = HybridPlannerComposition(llm.gateway)

        advisor = AdvisorComposition(
            portfolio=portfolio,
            scheme=scheme,
            customer=customer,
            planner=planner,
            tools=tools,
            prompt=prompt,
            llm=llm
        )

        _advisor =advisor
        return _advisor.agent
    
    return _advisor.agent


def get_advisor_service(
    orchestrator: Orchestrator=Depends(get_orchestrator)
) -> AdvisorService:

    return AdvisorService(
        orchestrator=orchestrator
    )