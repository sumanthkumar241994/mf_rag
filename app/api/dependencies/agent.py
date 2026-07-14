from fastapi import Depends
from app.agents.advisor_agent import AdvisorAgent
from app.api.dependencies.customer import get_customer_gateway
from app.api.dependencies.portfolio import get_portfolio_gateway
from app.api.dependencies.retrieval import get_context_builder, get_retrieval_service
from app.api.dependencies.scheme import get_scheme_gateway
from app.business.customer.gateway.falcon_customer_gateway import FalconCustomerGateway
from app.business.document.services.context_builder import ContextBuilder
from app.business.document.services.retrieval_service import RetrievalService
from app.business.goal.context.goal_context_provider import GoalContextProvider
from app.business.portfolio.gateways.falcon_portfolio_gateway import FalconPortfolioGateway
from app.business.portfolio.gateways.portfolio_gateway import PortfolioGateway
from app.business.scheme.gateways.falcon_scheme_gateway import FalconSchemeGateway
from app.composition.advisor_composition import AdvisorComposition
from app.composition.business.customer_composition import CustomerComposition
from app.composition.business.document_composition import DocumentComposition
from app.composition.business.goal_composition import GoalComposition
from app.composition.business.portfolio_composition import PortfolioComposition
from app.composition.business.scheme_composition import SchemeComposition
from app.composition.llm_composition.gemma_composition import LLMComposition
from app.composition.planner.deterministic_planner_composition import DeterministicPlannerComposition
from app.composition.prompt.advisor_prompt_composition import AdvisorPromptComposition
from app.composition.tool_composition import ToolComposition
from app.composition.workflow_composition import WorkflowComposition
from app.infrastructure.workflow.workflow_checkpointer import workflow_checkpointer

_advisor : AdvisorComposition | None = None

def get_advisor_agent(
    portfolio_gateway: FalconPortfolioGateway = Depends(get_portfolio_gateway),
    scheme_gateway: FalconSchemeGateway = Depends(get_scheme_gateway),
    customer_gateway: FalconCustomerGateway = Depends(get_customer_gateway),
    retrieval_service: RetrievalService = Depends(get_retrieval_service),
    context_builder: ContextBuilder = Depends(get_context_builder)
) -> AdvisorAgent:
    global _advisor
    if _advisor is None:
        workflow = WorkflowComposition()
        portfolio = PortfolioComposition(portfolio_gateway=portfolio_gateway, workflow_service=workflow.workflow_service)
        planner = DeterministicPlannerComposition()
        scheme = SchemeComposition(scheme_gateway=scheme_gateway, workflow_service=workflow.workflow_service)
        customer = CustomerComposition(customer_gateway=customer_gateway, workflow_service=workflow.workflow_service)
        goal_context = GoalContextProvider(customer_service=customer.customer_service, portfolio_service=portfolio.portofio_service)
        goal= GoalComposition(workflow_service=workflow.workflow_service, goal_context=goal_context)
        document = DocumentComposition(workflow_service=workflow.workflow_service, retrieval_service=retrieval_service, context_builder=context_builder)
        tools = ToolComposition()
        prompt = AdvisorPromptComposition()
        llm = LLMComposition()

        advisor = AdvisorComposition(
            portfolio=portfolio,
            scheme=scheme,
            customer=customer,
            goal=goal,
            document=document,
            planner=planner,
            tools=tools,
            prompt=prompt,
            llm=llm,
            workflow=workflow,
            checkpointer=workflow_checkpointer.checkpointer
        )

        _advisor =advisor
        return _advisor.agent
    
    return _advisor.agent