
from fastmcp import Client
from app.agents.investment_agent import InvestmentAgent
from app.api.dependencies.mcp import get_mcp
from app.composition.investment_composition import InvestmentComposition
from app.composition.mcp_clients.mcp_composition import MCPComposition
from app.infrastructure.workflow.workflow_checkpointer import workflow_checkpointer
from app.investment.workflows.investment_workflow import InvestmentWorkflow
from app.mcp.client.customer_client import CustomerClient
from app.mcp.client.mcp_client import MCPClient

_investment: InvestmentComposition | None = None

def investment_agent(
) -> InvestmentAgent:
    global _investment
    if _investment is None:
        mcp = get_mcp()
        investment = InvestmentComposition(
            mcp=mcp,
            checkpointer = workflow_checkpointer.checkpointer
        )

        _investment =investment
        return _investment.agent
    
    return _investment.agent


def get_investment_agent() -> InvestmentAgent:
    return investment_agent()