from __future__ import annotations

from langgraph.types import interrupt

from app.observability.tracing import trace_step
from app.workflows.advisor.advisor_state import AdvisorState
from app.workflows.workflow.models.workflow_execution import WorkflowExecution
from app.workflows.workflow.models.workflow_resume import WorkflowResume
from app.workflows.workflow.service.workflow_service import WorkflowService


class WorkflowNode:
    def __init__(self, workflow_service: WorkflowService):
        self._workflow_service = workflow_service

    
    @trace_step(
        "workflow",
        input_mapper=lambda self, state: (
            {
                "interrupted": (
                    state.workflow_execution.interrupted
                    if state.workflow_execution
                    else False
                ),
                "capability": (
                    state.workflow_execution.interrupt.capability.value
                    if state.workflow_execution
                    and state.workflow_execution.interrupt
                    else None
                ),
            }
        ),
        output_mapper=lambda state: {
            "status": (
                "interrupted"
                if state.workflow_interrupt
                else "completed"
            ),
        },
    )
    async def __call__(self, state: AdvisorState) -> AdvisorState:

        execution: WorkflowExecution | None = state.workflow_execution

        if execution is None:
            return state

        if not execution.interrupted:
            return state

        # Remove transient state before checkpoint
        state.customer = None
        state.portfolio_analysis = None

        # Optional
        state.prompt = None
        state.sources = []
        state.llm_response = None

        state.restore()
        print("Before interrupt")
        answer = interrupt(execution.interrupt)
        print("after interrupt")

        resumed_execution = await self._workflow_service.resume(
            state=state,
            capability=execution.interrupt.capability,
            payload=execution.interrupt.payload,
            resume=WorkflowResume(
                answer=answer,
            ),
        )

        state.workflow_execution = resumed_execution

        if resumed_execution.interrupted:
            state.workflow_interrupt = resumed_execution.interrupt
        else:
            state.workflow_interrupt = None

        return state