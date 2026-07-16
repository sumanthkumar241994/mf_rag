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


from typing import Any, AsyncIterator
from httpx import request
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command
from app.dtos.agents.stream_event import AgentStreamEvent
from app.enums.stream_event_type import StreamEventType
from app.enums.workflow_decision import WorkflowDecision
from app.mapper.advisor_state_mapper import AdvisorStateMapper
from app.workflows.advisor.advisor_state import AdvisorState
from app.workflows.advisor.nodes.guardrail_node import GuardRailNode
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
        guardrail_node: GuardRailNode,
        planner_node: PlannerNode,
        tool_exectution_node: ToolExecutionNode,
        workflow_node: WorkflowNode,
        tool_failure_node: ToolFailureNode,
        prompt_builder_node: PromptBuilderNode,
        llm_node: LLMNode,
        checkpointer: AsyncPostgresSaver
    ):
        self._guardrail_node = guardrail_node
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

        workflow.add_node("guardrails", self._guardrail_node)
        workflow.add_node("planner", self._planner_node)
        workflow.add_node("tool_execution", self._tool_execution_node)
        workflow.add_node("workflow", self._workflow_node)
        workflow.add_node("prompt_builder", self._prompt_builder_node)
        workflow.add_node("tool_failure", self._tool_failure_node)
        workflow.add_node("llm", self._llm_node)

        workflow.add_edge(START, "guardrails")
        workflow.add_conditional_edges(
            "guardrails",
            self._route_after_guardrails,
            {
                WorkflowDecision.CONTINUE.value: "planner",
                WorkflowDecision.END.value: END,
            },
        )
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

    
    def _route_after_guardrails(
    state: AdvisorState,
    ):
        if state.guardrail_result.allowed:
            return WorkflowDecision.CONTINUE.value

        return WorkflowDecision.END.value


    async def invoke(self, state: AdvisorState) -> AdvisorState:
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

    # async def stream(
    #     self,
    #     state: AdvisorState,
    # ) -> AsyncIterator[AgentStreamEvent]:

    #     async for event in self._graph.astream_events(
    #         state,
    #         config=WorkflowConfig.config(state),
    #         version="v2",
    #     ):

    #         stream_event = await self._handle_graph_event(
    #             state=state,
    #             event=event,
    #         )

    #         if stream_event is not None:
    #             yield stream_event


    async def stream(
        self,
        state: AdvisorState,
    ) -> AsyncIterator[AgentStreamEvent]:



        async for mode, chunk in self._graph.astream(
            state,
            config=WorkflowConfig.config(state),
            stream_mode=["updates", "custom"],
        ):


            # print("=" * 80)
            # print(mode)
            # print(chunk)
            # print("=" * 80)

            # if False:
            #     yield 

            # ----------------------------------------------------
            # Custom stream emitted from LLMNode
            # ----------------------------------------------------
            if mode == "custom":

                event = self._handle_custom_stream(
                    state=state,
                    chunk=chunk,
                )

                if event is not None:
                    yield event

                continue

            # ----------------------------------------------------
            # LangGraph state updates
            # ----------------------------------------------------
            if mode == "updates":

                async for event in self._handle_update_stream(
                    state=state,
                    chunk=chunk,
                ):
                    yield event

            

    async def resume_stream(
    self,
    state: AdvisorState,
    ) -> AsyncIterator[AgentStreamEvent]:

        async for mode, chunk in self._graph.astream(
            Command(
                resume=state.request.workflow_resume,
            ),
            config=WorkflowConfig.config(state),
            stream_mode=["updates", "custom"],
        ):

            if mode == "custom":

                event = self._handle_custom_stream(
                    state=state,
                    chunk=chunk,
                )

                if event is not None:
                    yield event

                continue

            if mode == "updates":

                async for event in self._handle_update_stream(
                    state=state,
                    chunk=chunk,
                ):
                    yield event

    # async def _handle_graph_event(
    #     self,
    #     state: AdvisorState,
    #     event: dict[str, Any],
    # ) -> AgentStreamEvent | None:

    #     print("=" * 80)
    #     print(f"Event     : {event.get('event')}")
    #     print(f"Name      : {event.get('name')}")
    #     print(f"Run ID    : {event.get('run_id')}")
    #     print(f"Parent ID : {event.get('parent_ids')}")
    #     print("=" * 80)

    #     return None

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



    def _handle_custom_stream(
        self,
        state: AdvisorState,
        chunk: dict[str, Any],
    ) -> AgentStreamEvent | None:

        stream_type = chunk.get("type")

        if stream_type =='prompt_start':
            
            return AgentStreamEvent(
                type=StreamEventType.PROMPT_START.value
            )

        if stream_type == "token":
            return AgentStreamEvent(
                type=StreamEventType.TOKEN.value,
                token=chunk["token"],
            )

        if stream_type == "completed":
            return AgentStreamEvent(
                type=StreamEventType.COMPLETED.value,
                response=chunk["response"],
            )

        if stream_type == "error":
            return AgentStreamEvent(
                type=StreamEventType.ERROR.value,
                message=chunk["message"],
            )

        return None


    async def _handle_update_stream(
        self,
        state: AdvisorState,
        chunk: dict[str, Any],
    ) -> AsyncIterator[AgentStreamEvent]:


        if "__interrupt__" in chunk:

            interrupt = chunk["__interrupt__"][0]

            yield AgentStreamEvent(
                type=StreamEventType.WORKFLOW_INTERRUPT.value,
                workflow_interrupt=interrupt.value,
            )

            return


        node_name = next(iter(chunk))
        node_state = chunk[node_name]

        if node_name == "guardrails":
            llm_response = node_state.get("llm_response")
            if llm_response:
                yield AgentStreamEvent(
                    type=StreamEventType.COMPLETED.value,
                    response=llm_response,
                )

                return

        elif node_name == "planner":

            planner = node_state["planner_result"]

            yield AgentStreamEvent(
                type=StreamEventType.PLANNER_END.value,
                metadata={
                    "intent": planner.intent.value,
                    "tools": [t.value for t in planner.selected_tools],
                    "confidence": planner.confidence,
                },
            )

        elif node_name == "tool_execution":

            for result in node_state["tool_results"]:

                yield AgentStreamEvent(
                    type=StreamEventType.TOOL_END.value,
                    tool=result["tool"],
                    success=result["success"],
                    metadata={
                        "execution_time_ms": result["execution_time_ms"],
                    },
                )

        elif node_name == "prompt_builder":

            prompt = node_state["prompt"]

            yield AgentStreamEvent(
                type=StreamEventType.PROMPT_END.value,
                metadata={
                    "prompt_length": len(prompt.user_prompt),
                },
            )

        elif node_name == "tool_failure":

            errors = node_state["errors"]

            message = (
                errors[-1].message
                if errors
                else "Unable to execute the requested tool."
            )

            yield AgentStreamEvent(
                type=StreamEventType.ERROR.value,
                message=message,
            )
            

    # async def _handle_update_stream(
    #     self,
    #     state: AdvisorState,
    #     chunk: dict[str, Any],
    # ) -> AsyncIterator[AgentStreamEvent]:

    #     from pprint import pprint

    #     print("=" * 80)
    #     pprint(chunk)
    #     print("=" * 80)

    #     if False:
    #         yield

        # #
        # # Planner completed
        # #
        # if "planner" in chunk:

        #     yield AgentStreamEvent(
        #         type=StreamEventType.PLANNER_END.value,
        #         metadata={
        #             "intent": state.planner_result.intent.value,
        #             "tools": [
        #                 tool.value
        #                 for tool in state.planner_result.selected_tools
        #             ],
        #             "confidence": state.planner_result.confidence,
        #         },
        #     )

        #     return

        # #
        # # Tool execution completed
        # #
        # if "tool_execution" in chunk:

        #     for result in state.tool_results:

        #         yield AgentStreamEvent(
        #             type=StreamEventType.TOOL_END.value,
        #             tool=result["tool"],
        #             success=result["success"],
        #             metadata={
        #                 "execution_time_ms": result["execution_time_ms"],
        #             },
        #         )

        #     return

        # #
        # # Prompt built
        # #
        # if "prompt_builder" in chunk:

        #     yield AgentStreamEvent(
        #         type=StreamEventType.PROMPT_END.value,
        #         metadata={
        #             "prompt_length": len(state.prompt.user_prompt),
        #         },
        #     )

        #     return

        # #
        # # Tool failure
        # #
        # if "tool_failure" in chunk:

        #     if state.errors:
        #         message = state.errors[-1].message
        #     else:
        #         message = "Unable to execute the requested tool."

        #     yield AgentStreamEvent(
        #         type=StreamEventType.ERROR.value,
        #         message=message,
        #     )

        #     return

        # #
        # # LLM finished
        # #
        # if "llm" in chunk:

        #     # Nothing to emit.
        #     # COMPLETED comes from the custom stream.
        #     return