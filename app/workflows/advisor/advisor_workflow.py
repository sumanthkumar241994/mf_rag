# from langgraph.graph import StateGraph, START, END
# from app.workflows.advisor.advisor_state import AdvisorState


# from app.workflows.nodes.context.build_context_node import BuildContextNode
# from app.workflows.nodes.llm.generate_answer_node import GenerateAnswerNode
# from app.workflows.nodes.retrieval.document_search_node import DocumentSearchNode

# class AdvisorWorkflow:

#     def __init__(
#         self,
#         planner_node: Planner,
#         build_context_node: BuildContextNode,
#         generate_answer_node: GenerateAnswerNode
#     ):
#         self.document_search_node = document_search_node
#         self.build_context_node = build_context_node
#         self.generate_answer_node = generate_answer_node

#         self.graph = self._build_graph()

    
#     def _build_graph(self):

#         workflow = StateGraph(AdvisorState)

#         workflow.add_node("document_search", self.document_search_node)
#         workflow.add_node("build_context", self.build_context_node)
#         workflow.add_node("generate_answer", self.generate_answer_node)

#         workflow.add_edge(START, "document_search")
#         workflow.add_edge("document_search", "build_context")
#         workflow.add_edge("build_context", "generate_answer")
#         workflow.add_edge("generate_answer", END)

#         return workflow.compile()

#     async def invoke(self, request: AgentRequest) -> WorkflowResponse:
#         state: AdvisorState = {"query": request.query, "history": request.conversation}
#         state = await self.graph.ainvoke(state)

#         return WorkflowResponse(
#             answer=state['answer'],
#             sources=state["sources"],
#             retrieved_chunks=len(state["chunks"]),
#             llm_usage=state.get("llm_usage"),
#             llm_metrics=state['llm_metrics']
#         )

#     async def stream(self, request: AgentRequest):
#         state = await self._prepare_state(request)
#         # stream answer
#         async for event in self.generate_answer_node.stream(state):
#             yield event
        
#     async def _prepare_state(self, request: AgentRequest) -> AdvisorState:
#         state: AdvisorState = {"query": request.query, "history": request.conversation}
#         state.update(await self.document_search_node(state))
#         state.update(await self.build_context_node(state))

#         return state


from langgraph.graph import StateGraph, START, END
from app.enums.workflow_decision import WorkflowDecision
from app.workflows.advisor.advisor_state import AdvisorState
from app.workflows.advisor.nodes.llm_node import LLMNode
from app.workflows.advisor.nodes.planner_node import PlannerNode
from app.workflows.advisor.nodes.prompt_builder_node import PromptBuilderNode
from app.workflows.advisor.nodes.tool_execution_node import ToolExecutionNode
from app.workflows.advisor.nodes.tool_failure_node import ToolFailureNode



class AdvisorWorkflow:

    def __init__(
        self,
        planner_node: PlannerNode,
        tool_exectution_node: ToolExecutionNode,
        tool_failure_node: ToolFailureNode,
        prompt_builder_node: PromptBuilderNode,
        llm_node: LLMNode
    ):
        self._planner_node = planner_node
        self._tool_execution_node = tool_exectution_node
        self._tool_failure_node = tool_failure_node
        self._prompt_builder_node = prompt_builder_node
        self._llm_node = llm_node
        self._graph = self._build_graph()

    
    def _build_graph(self):

        workflow = StateGraph(AdvisorState)

        workflow.add_node("planner", self._planner_node)
        workflow.add_node("tool_execution", self._tool_execution_node)
        workflow.add_node("prompt_builder", self._prompt_builder_node)
        workflow.add_node("tool_failure", self._tool_failure_node)
        workflow.add_node("llm", self._llm_node)

        workflow.add_edge(START, "planner")
        workflow.add_edge("planner", "tool_execution")
        workflow.add_conditional_edges(
            "tool_execution", 
            self._route_after_tool_execution,
            {
                WorkflowDecision.CONTINUE.value: "prompt_builder",
                WorkflowDecision.TOOL_FAILURE.value: "tool_failure"
            }
        )
        workflow.add_edge("prompt_builder", "llm")
        workflow.add_edge("llm", END)
        workflow.add_edge("tool_failure", END)

        return workflow.compile()

    def _route_after_tool_execution(
        self,
        state: AdvisorState,
    ) -> str:

        successful_tools = {
            result["tool"]
            for result in state.tool_results
            if result["success"]
        }

        for tool in state.planner_result.selected_tools:
            if tool not in successful_tools:
                return WorkflowDecision.TOOL_FAILURE.value

        return WorkflowDecision.CONTINUE.value


    async def invoke(self, state: AdvisorState) -> AdvisorState:
        result = await self._graph.ainvoke(state)
        print(result)
        if isinstance(result, dict):
            return AdvisorState(**result)

        return result


    async def stream(self, state: AdvisorState):
        pass
        # async for event in self.generate_answer_node.stream(state):
        #     yield event
