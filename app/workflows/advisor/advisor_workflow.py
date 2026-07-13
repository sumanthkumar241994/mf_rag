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


from typing import AsyncIterator
from httpx import request
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command
from app.dtos.agents.stream_event import AgentStreamEvent
from app.enums.workflow_decision import WorkflowDecision
from app.mapper.advisor_state_mapper import AdvisorStateMapper
from app.workflows.advisor.advisor_state import AdvisorState
from app.workflows.advisor.nodes.llm_node import LLMNode
from app.workflows.advisor.nodes.planner_node import PlannerNode
from app.workflows.advisor.nodes.prompt_builder_node import PromptBuilderNode
from app.workflows.advisor.nodes.tool_execution_node import ToolExecutionNode
from app.workflows.advisor.nodes.tool_failure_node import ToolFailureNode
from app.workflows.workflow.node.workflow_node import WorkflowNode

from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from app.workflows.workflow_config import WorkflowConfig



class AdvisorWorkflow:

    def __init__(
        self,
        planner_node: PlannerNode,
        tool_exectution_node: ToolExecutionNode,
        workflow_node: WorkflowNode,
        tool_failure_node: ToolFailureNode,
        prompt_builder_node: PromptBuilderNode,
        llm_node: LLMNode,
        checkpointer: AsyncPostgresSaver
    ):
        self._planner_node = planner_node
        self._tool_execution_node = tool_exectution_node
        self._workflow_node = workflow_node
        self._tool_failure_node = tool_failure_node
        self._prompt_builder_node = prompt_builder_node
        self._llm_node = llm_node
        self._checkpointer = checkpointer
        self._graph = self._build_graph()

    
    def _build_graph(self):

        workflow = StateGraph(AdvisorState)

        workflow.add_node("planner", self._planner_node)
        workflow.add_node("tool_execution", self._tool_execution_node)
        workflow.add_node("workflow", self._workflow_node)
        workflow.add_node("prompt_builder", self._prompt_builder_node)
        workflow.add_node("tool_failure", self._tool_failure_node)
        workflow.add_node("llm", self._llm_node)

        workflow.add_edge(START, "planner")
        workflow.add_edge("planner", "tool_execution")
        workflow.add_conditional_edges(
            "tool_execution", 
            self._route_after_tool_execution,
            {
                WorkflowDecision.CONTINUE.value: "workflow",
                WorkflowDecision.TOOL_FAILURE.value: "tool_failure"
            }
        )
        workflow.add_edge("workflow", "prompt_builder")
        workflow.add_edge("prompt_builder", "llm")
        workflow.add_edge("llm", END)
        workflow.add_edge("tool_failure", END)

        return workflow.compile(
            checkpointer=self._checkpointer
        )

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
            if tool.value not in successful_tools:
                return WorkflowDecision.TOOL_FAILURE.value

        return WorkflowDecision.CONTINUE.value


    async def invoke(self, state: AdvisorState) -> AdvisorState:
        print(WorkflowConfig.config(state))

        result = await self._graph.ainvoke(
            state,
            config=WorkflowConfig.config(state)
        )
        print(result)
        if isinstance(result, dict):
            result = {
                key: value
                for key, value in result.items()
                if not key.startswith("__")
            }
            return AdvisorStateMapper.from_dict(result)

        return result
        

    async def resume(
        self,
        state: AdvisorState,
        answer: str,
    ) -> AdvisorState:

        config = WorkflowConfig.config(state)

        snapshot = await self._graph.aget_state(config)

        # Workflow already completed
        if snapshot.next == ():
            restored = AdvisorStateMapper.from_dict(snapshot.values)

            # If we already have an answer, simply return it.
            if restored.llm_response is not None:
                return restored

            # Otherwise there is nothing to resume.
            return restored

        result = await self._graph.ainvoke(
            Command(resume=answer),
            config=config,
        )

        if isinstance(result, dict):
            return AdvisorStateMapper.from_dict(result)

        return result


    # async def stream(self, state: AdvisorState) -> AsyncIterator[AgentStreamEvent]:

    #     async for event in self._planner_node.stream(state):
    #         yield event
        
    #     async for event in self._tool_execution_node.stream(state):
    #         yield event

    #     if self._route_after_tool_execution(state) == WorkflowDecision.TOOL_FAILURE.value:
    #         async for event in self._tool_failure_node.stream(state):
    #             yield event
            
    #         return

    #     # workflow (Goal Interrupt today)
    #     await self._workflow_node(state)

    #     async for event in self._prompt_builder_node.stream(state):
    #         yield event
        

    #     async for event in self._llm_node.stream(state):
    #         yield event

    async def stream(self, state: AdvisorState) -> AsyncIterator[AgentStreamEvent]:

        async for event in self._graph.astream_events(
            state,
            config=WorkflowConfig.config(state),
            version="v2",
        ):
            yield await self._handle_graph_event(event)

    async def resume_stream(self, state: AdvisorState) -> AsyncIterator[AgentStreamEvent]:

        async for event in self._graph.astream_events(
            Command(
                resume=state.request.workflow_resume,
            ),
            config=WorkflowConfig.config(state),
            version="v2",
        ):
            yield await self._handle_graph_event(event)
