from langgraph.graph import StateGraph, START, END
from app.workflows.advisor.advisor_state import AdvisorState

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

    async def invoke(self, query: str) -> AdvisorState:
        return await self.graph.ainvoke({"query": query})

    async def stream(self, query: str):
        state: AdvisorState = {"query": query}

        state.update(await self.document_search_node(state))
        state.update(await self.build_context_node(state))
        # stream answer
        async for token in self.generate_answer_node.stream(state):
            yield token