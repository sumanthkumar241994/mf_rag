

from langgraph.checkpoint.base import BaseCheckpointSaver
from app.agents.investment_agent import InvestmentAgent
from app.composition.mcp_clients.customer_client_composition import CustomerClientComposition
from app.investment.workflows.investment_workflow import InvestmentWorkflow
from app.investment.workflows.nodes.customer_node import CustomerNode
from app.mcp.client.mcp_client import MCPClient


class InvestmentComposition:
    """
    Composition root for the Advisor workflow.

    Responsible only for wiring the application together.
    """

    def __init__(
        self,
        mcp: MCPClient,
        checkpointer: BaseCheckpointSaver,
    ):
        
        self.customer_client = CustomerClientComposition(mcp)

        self._customer_node = CustomerNode(
            customer_client= self.customer_client.client
        )

        
        self.workflow = InvestmentWorkflow(
            customer_node=self._customer_node,
            checkpointer=checkpointer,
        )

        self.agent = InvestmentAgent(
            investment_workflow=self.workflow
        )