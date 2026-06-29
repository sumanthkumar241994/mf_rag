from langgraph.graph import StateGraph, START, END
from app.workflows.advisor.advisor_state import AdvisorState

from app.dtos.agents.agent_request import AgentRequest
from app.dtos.workflow.workflow_response import WorkflowResponse

from app.workflows.nodes.context.build_context_node import BuildContextNode
from app.workflows.nodes.llm.generate_answer_node import GenerateAnswerNode
from app.workflows.nodes.retrieval.document_search_node import DocumentSearchNode

class AdvisorWorkflow:

    def __init__(
        self,
        document_search_node: DocumentSearchNode,
        build_context_node: BuildContextNode,
        generate_answer_node: GenerateAnswerNode
    ):
        self.document_search_node = document_search_node
        self.build_context_node = build_context_node
        self.generate_answer_node = generate_answer_node

        self.graph = self._build_graph()

    
    def _build_graph(self):

        workflow = StateGraph(AdvisorState)

        workflow.add_node("document_search", self.document_search_node)
        workflow.add_node("build_context", self.build_context_node)
        workflow.add_node("generate_answer", self.generate_answer_node)

        workflow.add_edge(START, "document_search")
        workflow.add_edge("document_search", "build_context")
        workflow.add_edge("build_context", "generate_answer")
        workflow.add_edge("generate_answer", END)

        return workflow.compile()

    async def invoke(self, request: AgentRequest) -> WorkflowResponse:
        state: AdvisorState = {"query": request.query, "history": request.conversation}
        state = await self.graph.ainvoke(state)

        return WorkflowResponse(
            answer=state['answer'],
            sources=state["sources"],
            retrieved_chunks=len(state["chunks"]),
            llm_usage=state.get("llm_usage"),
            llm_metrics=state['llm_metrics']
        )

    async def stream(self, request: AgentRequest):
        state = await self._prepare_state(request)
        # stream answer
        async for event in self.generate_answer_node.stream(state):
            yield event
        
    async def _prepare_state(self, request: AgentRequest) -> AdvisorState:
        state: AdvisorState = {"query": request.query, "history": request.conversation}
        state.update(await self.document_search_node(state))
        state.update(await self.build_context_node(state))

        return state
