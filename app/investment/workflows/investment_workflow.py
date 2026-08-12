from typing import Any, AsyncIterator

from langgraph.types import Command
from app.dtos.agents.stream_event import AgentStreamEvent
from app.dtos.llm.llm_stream_response import LLMStreamResponse
from app.enums.stream_event_type import StreamEventType
from app.investment.workflows.investment_state import InvestmentState
from app.investment.workflows.models.workflow_interrupt import WorkflowInterrupt
from app.investment.workflows.nodes.customer_node import CustomerNode
from langgraph.graph import END, START, StateGraph
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

from app.investment.workflows.nodes.data_collection_node import DataCollectionNode
from app.investment.workflows.nodes.eligbility_node import EligibilityNode
from app.investment.workflows.nodes.verification_node import VerificationNode
from app.investment.workflows.nodes.verification_prepare_node import VerificationPrepareNode
from app.investment.workflows.nodes.verification_wait_node import VerificationWaitNode
from app.observability.tracing import trace_step
from app.workflows.workflow_config import WorkflowConfig


class InvestmentWorkflow:

    def __init__(
        self,
        customer_node: CustomerNode,
        eligibility_node: EligibilityNode,
        data_collection_node: DataCollectionNode,
        verification_prepare_node: VerificationPrepareNode,
        verification_wait_node: VerificationWaitNode,
        checkpointer: AsyncPostgresSaver,
    ):
        self._customer_node = customer_node
        self._eligibility_node = eligibility_node
        self._data_collection_node = data_collection_node
        self._verification_prepare_node = verification_prepare_node
        self._verification_wait_node = verification_wait_node
        self._checkpointer = checkpointer
        self._graph = self._build_graph()

    def _build_graph(self):

        workflow = StateGraph(InvestmentState)
        workflow.add_node("customer", self._customer_node)
        workflow.add_node("eligibility", self._eligibility_node)
        workflow.add_node("data_collection", self._data_collection_node)
        workflow.add_node("verification_prepare", self._verification_prepare_node)
        workflow.add_node("verification_wait", self._verification_wait_node)

        workflow.add_edge(START, "customer")
        workflow.add_conditional_edges(
            "customer",
            self._route_after_customer,
            {
                END: END,
                "eligibility": "eligibility",
                "verification": "verification_prepare",
                "data_collection": "data_collection",
            },
        )
        workflow.add_conditional_edges(
            "eligibility",
            self._route_after_eligibility,
            {
                END: END,
                "data_collection": "data_collection",
                "verification": "verification_prepare",
            },
        )
        workflow.add_conditional_edges(
            "data_collection",
            self._route_after_data_collection,
            {
                "verification": "verification_prepare",
                "customer": "customer",
                END: END,
            },
        )
        workflow.add_edge( "verification_prepare", "verification_wait")
        workflow.add_edge("verification_wait", "customer" )

        # workflow.add_conditional_edges(
        #     "eligibility",
        #     self._route_after_eligibility,
        #     {
        #         END: END,
        #         "investment": "investment",
        #     },
        # )
        
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

    async def resume(self, state: InvestmentState) -> InvestmentState:

        config = WorkflowConfig.config(state)

        snapshot = await self._graph.aget_state(config)

        # Workflow already completed
        if snapshot.next == ():
            return InvestmentState.model_validate(
                snapshot.values,
            )

        result = await self._graph.ainvoke(
            Command(
                resume=state.request.workflow_resume,
            ),
            config=config,
        )

        if isinstance(result, dict):
            return InvestmentState.model_validate(
                result,
            )

        return result

    
    async def stream(
        self,
        state: InvestmentState,
    ) -> AsyncIterator[AgentStreamEvent]:

        async for _, chunk in self._graph.astream(
            state,
            config=WorkflowConfig.config(state),
            stream_mode=["updates"],
        ):

            async for event in self._handle_update_stream(
                state=state,
                chunk=chunk,
            ):
                yield event

    async def resume_stream(
    self,
    state: InvestmentState,
    ) -> AsyncIterator[AgentStreamEvent]:

        config = WorkflowConfig.config(state)

        snapshot = await self._graph.aget_state(config)

        #
        # Workflow already completed.
        #
        # if snapshot.next == ():
        #     return

        has_interrupt = bool(snapshot.interrupts)

        if not has_interrupt:
            has_interrupt = any(task.interrupts for task in snapshot.tasks)

        if not has_interrupt:
            return

        workflow_resume = state.request.workflow_resume

        if workflow_resume is None:
            raise ValueError(
                "Workflow resume data is required."
            )

        async for _, chunk in self._graph.astream(
            Command(
                resume=state.request.workflow_resume,
            ),
            config=config,
            stream_mode=["updates"],
        ):

            async for event in self._handle_update_stream(
                state=state,
                chunk=chunk,
            ):
                yield event


    async def _handle_update_stream(
    self,
    state: InvestmentState,
    chunk: dict[str, Any],
    ) -> AsyncIterator[AgentStreamEvent]:

        if "__interrupt__" in chunk:

            interrupt = chunk["__interrupt__"][0]
            workflow_interrupt = WorkflowInterrupt.model_validate(interrupt.value)

            yield AgentStreamEvent(
                type=StreamEventType.WORKFLOW_INTERRUPT.value,
                workflow_interrupt=workflow_interrupt,
            )

            return


        # LangGraph emits the updated state for the node.
        node_name = next(iter(chunk))
        node_state = chunk[node_name]

        # Synchronize workflow state.
        state.workflow_execution = node_state.get(
            "workflow_execution",
            state.workflow_execution,
        )

        state.last_error = node_state.get(
            "last_error",
            state.last_error,
        )

        # Workflow failed.
        if state.last_error is not None:

            yield AgentStreamEvent(
                type=StreamEventType.COMPLETED.value,
                response=LLMStreamResponse(
                    answer=state.last_error.message,
                ),
                metadata={
                    "response_type": "workflow_error",
                    "source": state.last_error.source,
                    "code": state.last_error.code,
                },
            )

            return

        execution = state.workflow_execution

        if execution is None:
            return

        # Workflow interrupted.
        # if execution.interrupted:

        #     yield AgentStreamEvent(
        #         type=StreamEventType.WORKFLOW_INTERRUPT.value,
        #         workflow_interrupt=execution.interrupt,
        #     )

        #     return

        # Workflow completed successfully.
        # yield AgentStreamEvent(
        #     type=StreamEventType.WORKFLOW_COMPLETED.value,
        #     workflow_execution=execution,
        # )

    
    def _route_after_customer(
    self,
    state: InvestmentState,
    ) -> str:

        if state.last_error is not None:
            return END

        if state.workflow_execution and state.workflow_execution.interrupted:
            return END

        # No active execution goal means we need to determine
        # what customer requirement comes next.
        if state.execution_goal is None:

            if state.pending_actions:
                return "data_collection"

            return "eligibility"

        # Active execution requires verification.
        if (
            state.execution_goal.requires_verification
            and (
                state.verification is None
                or not state.verification.verified
            )
        ):
            return "verification"

        return "customer"


    def _route_after_eligibility(
    self,
    state: InvestmentState,
    ) -> str:

        execution = state.workflow_execution

        if execution and execution.interrupted:
            return END

        return "investment"

    def _route_after_eligibility(self, state: InvestmentState) -> str:
        if state.eligibility and state.eligibility.required:
            return "data_collection"

        return "customer"
    


    def _route_after_data_collection(
        self,
        state: InvestmentState,
    ) -> str:

        # Data collection has created an execution goal.
        if state.execution_goal is None:
            return END

        # The selected action requires OTP verification.
        if state.execution_goal.requires_verification:
            return "verification"

        # No verification required.
        return "customer"