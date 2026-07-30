from typing import AsyncIterator
from app.dtos.agents.stream_event import AgentStreamEvent
from app.investment.workflows.investment_state import InvestmentState
from app.investment.workflows.nodes.customer_node import CustomerNode
from langgraph.graph import END, START, StateGraph
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from app.observability.tracing import trace_step
from app.workflows.workflow_config import WorkflowConfig


class InvestmentWorkflow:

    def __init__(
        self,
        customer_node: CustomerNode,
        checkpointer: AsyncPostgresSaver,
    ):
        self._customer_node = customer_node
        self._checkpointer = checkpointer
        self._graph = self._build_graph()

    def _build_graph(self):

        workflow = StateGraph(InvestmentState)
        workflow.add_node("customer", self._customer_node)
        workflow.add_edge(START, "customer")
        workflow.add_edge("customer", END)

        return workflow.compile(
            checkpointer=self._checkpointer,
        )

    @trace_step(
        "investment_workflow",
        output_mapper=lambda state: {
            "errors": len(state.errors),
            "workflow_execution": state.workflow_execution is not None,
        },
    )
    async def invoke(self, state: InvestmentState) -> InvestmentState:

        result = await self._graph.ainvoke(
            state,
            config=WorkflowConfig.config(state),
        )

        if isinstance(result, dict):
            result = {
                key: value
                for key, value in result.items()
                if not key.startswith("__")
            }

        return result

    
    async def stream(
        self,
        state: InvestmentState,
    ) -> AsyncIterator[AgentStreamEvent]:

        async for event in self._graph.astream_events(
            state,
            config=WorkflowConfig.config(state),
            version="v2",
        ):

            print("=" * 80)
            print(event)
            print("=" * 80)

            if False:
                yield 
