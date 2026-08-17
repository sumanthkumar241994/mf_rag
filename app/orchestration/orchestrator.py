from dataclasses import asdict, replace
import time
from typing import AsyncIterator
from uuid import UUID

from app.agents.advisor_agent import AdvisorAgent
from app.agents.base_agent import BaseAgent
from app.agents.investment_agent import InvestmentAgent
from app.agents.router.agent_router import AgentRouter
from app.ai.guardrails.deterministic.models.guardrail_result import GuardRailResult
from app.ai.guardrails.guardrail_service import GuardRailService
from app.business.advisor.enums.agent_type import AgentType
from app.core.middleware.request_context_vars import trace_id_ctx
from app.dtos.agents.agent_plan import AgentPlan
from app.dtos.agents.agent_request import AgentRequest
from app.dtos.agents.stream_event import AgentStreamEvent
from app.dtos.llm.llm_stream_response import LLMStreamResponse
from app.dtos.request_context import RequestContext
from app.enums.stream_event_type import StreamEventType
from app.dtos.agents.agent_response import AgentResponse
from app.enums.workflow import WorkflowType
from app.investment.workflows.models.delegation import Delegation
from app.models.conversation import Conversation
from app.models.message import Message
from app.services.conversation_service import ConversationService
from app.workflows.advisor.advisor_state import AdvisorState

import app.observability.langfuse_helper as LangfuseHelper


class Orchestrator:
    def __init__(
        self, 
        conversation_service: ConversationService, 
        guardrail_service: GuardRailService,
        agent_router: AgentRouter,
        advisor_agent: AdvisorAgent,
        investment_agent: InvestmentAgent
    ):
        self.conversation_service = conversation_service
        self._guardrail_service = guardrail_service
        self._agent_router = agent_router
        self._agents: dict[AgentType, BaseAgent] = {
            AgentType.ADVISOR: advisor_agent,
            AgentType.INVESTMENT: investment_agent,
        }
        self._workflow_agent_mapping: dict[WorkflowType, AgentType] = {
            WorkflowType.ADVISOR: AgentType.ADVISOR,
            WorkflowType.INVESTMENT_PURCHASE: AgentType.INVESTMENT,
            WorkflowType.INVESTMENT_REDEMPTION: AgentType.INVESTMENT,
            WorkflowType.INVESTMENT_SWITCH: AgentType.INVESTMENT,
            WorkflowType.INVESTMENT_STP: AgentType.INVESTMENT,
            WorkflowType.INVESTMENT_SWP: AgentType.INVESTMENT,
        }

    async def run(self, request: RequestContext) -> AgentResponse:
        start_time = time.perf_counter() 

        trace_id = LangfuseHelper.get_trace_id()

        conversation = await self.conversation_service.get_or_create_conversation(
                            customer_id=request.customer_id,
                            conversation_id=request.conversation_id,
                            workflow='advisor'
                        )

        if request.workflow_resume:
            await self.conversation_service.add_resume_message(
                conversation=conversation,
                content=request.workflow_resume,
                trace_id=trace_id   
            )
        else:
            await self.conversation_service.add_user_message(
                conversation=conversation,
                content=request.query,
                trace_id=trace_id
            )

        result = await self._guardrail_service.validate(request_context=request)

        request.conversation_id = conversation.id
        trace_id_ctx.set(trace_id)

        if not result.allowed:
            response_time_ms = round((time.perf_counter()-start_time) *1000)
            metadata = {
                "response_type": "guardrail",
                "guardrail": result.category,
                "reason": result.reason,
            }
            response = AgentResponse(
                conversation_id=conversation.id,
                answer=result.response,
                response_time_ms=response_time_ms,
                metadata=metadata
            )

            await self.conversation_service.add_assistant_message(
                conversation=conversation,
                content=result.response,
                trace_id=trace_id,
                metadata=metadata
            )
            
            return response


        history = await self.conversation_service.get_recent_context(conversation.id)

        agent_request = AgentRequest(
            request=request,
            conversation=history,
        )

        plan = await self._agent_router.route(agent_request)
        agent = self._get_agent(plan.primary_agent)
        state = agent.create_state(request=request, history=history, trace_id=trace_id)

        state.metadata["agent_plan"] = plan.to_dict()


        if request.workflow_resume:
            response = await agent.resume(state)
        else:
            response = await agent.run(state)

        if response.answer:
            response.metadata["agent_plan"] = state.metadata["agent_plan"]

            await self.conversation_service.add_assistant_message(
                conversation=conversation,
                content=response.answer,
                trace_id=trace_id,
                metadata=response.metadata
            )
        response.response_time_ms = round((time.perf_counter()-start_time) *1000)
        
        return response

    async def stream(self, request: RequestContext) -> AsyncIterator[AgentStreamEvent]:
        trace_id = LangfuseHelper.get_trace_id()

        conversation = await self.conversation_service.get_or_create_conversation(
                customer_id=request.customer_id,
                conversation_id=request.conversation_id,
                workflow=None,
            )

        request.conversation_id = conversation.id
        trace_id_ctx.set(trace_id)

        # Resume Workflow
        if request.workflow_resume:
            agent = await self._resolve_resume_agent(conversation)

            await self.conversation_service.add_resume_message(
                conversation=conversation,
                content=request.workflow_resume,
                trace_id=trace_id,
            )

            plan = None

        # New / Follow-up Query
        else:
            await self.conversation_service.add_user_message(
                conversation=conversation,
                content=request.query,
                trace_id=trace_id,
            )

            result = await self._guardrail_service.validate(request_context=request)

            if not result.allowed:
                async for event in self._run_guardrails(
                    conversation=conversation,
                    result=result,
                    trace_id=trace_id,
                ):
                    yield event

                return

            agent, plan = await self._resolve_agent(request=request, conversation=conversation)

        history = await self.conversation_service.get_recent_context(conversation.id)

        state = agent.create_state(
            request=request,
            history=history,
            trace_id=trace_id,
        )

        if plan is not None:
            state.metadata["agent_plan"] = plan.to_dict()

        yield AgentStreamEvent(
            type=StreamEventType.SESSION.value,
            metadata={
                "conversation_id": str(conversation.id),
                "trace_id": trace_id,
            },
        )

        stream = agent.resume_stream(state) if request.workflow_resume else agent.stream(state)

        stream_response = None
        workflow_interrupt = None

        async for event in stream:

            # -----------------------------------------------------
            # Workflow delegation
            # -----------------------------------------------------

            if event.type == StreamEventType.WORKFLOW_DELEGATION.value:

                delegation = event.workflow_delegation

                await self._handle_delegation(
                    conversation_id=conversation.id,
                    delegation=delegation,
                )

                # Current workflow is finished.
                #
                # Start the delegated workflow immediately.
                # The frontend does not need to know about the
                # internal delegation event.
                async for delegated_event in (
                    self._stream_delegated_workflow(
                        conversation=conversation,
                        request=request,
                        delegation=delegation,
                        trace_id=trace_id,
                    )
                ):
                    yield delegated_event

                return

            yield event


            if event.type == StreamEventType.COMPLETED.value:
                stream_response = event.response

            elif event.type == StreamEventType.WORKFLOW_INTERRUPT.value:
                workflow_interrupt = event.workflow_interrupt
                break

        if stream_response:
            metadata = {}

            if plan is not None:
                metadata["agent_plan"] = plan.to_dict()

            if stream_response.usage:
                metadata["llm_usage"] = asdict(stream_response.usage)

            if stream_response.metrics:
                metadata["llm_metrics"] = asdict(stream_response.metrics)

            message = (
                await self.conversation_service.add_assistant_message(
                    conversation=conversation,
                    content=stream_response.answer,
                    trace_id=trace_id,
                    metadata=metadata,
                )
            )

            yield AgentStreamEvent(
                type=StreamEventType.MESSAGE_SAVED.value,
                metadata={
                    "message_id": str(message.id),
                },
            )

        elif workflow_interrupt:
            await self.conversation_service.add_interrupt_message(
                conversation=conversation,
                workflow_interrupt=workflow_interrupt,
                trace_id=trace_id,
            )

    async def _resolve_agent(self, request: RequestContext, conversation: Conversation) -> tuple[BaseAgent, AgentPlan]:
        history = await self.conversation_service.get_recent_context(conversation.id)
        plan = await self._agent_router.route(
            AgentRequest(
                request=request,
                conversation=history,
            )
        )

        workflow = plan.workflow.value if plan.workflow else None

        if conversation.workflow != workflow:
            await self.conversation_service.update_workflow(
                conversation_id=conversation.id,
                workflow=workflow,
            )

        return (self._get_agent(plan.primary_agent), plan)

    async def _run_guardrails(self, result: GuardRailResult, conversation: Conversation, trace_id: str) -> AgentStreamEvent:

        metadata = {
            "response_type": "guardrail",
            "blocked": True,
            "category": (
                result.category.value
                if result.category
                else None
            ),
            "validator": result.validator,
            "reason": result.reason,
        }

        yield AgentStreamEvent(
            type=StreamEventType.COMPLETED.value,
            response=LLMStreamResponse(
                answer=result.response,
            ),
            metadata=metadata,
        )

        message = await self.conversation_service.add_assistant_message(
            conversation=conversation,
            content=result.response,
            trace_id=trace_id,
            metadata=metadata,
        )

        yield AgentStreamEvent(
            type=StreamEventType.MESSAGE_SAVED.value,
            metadata={
                "message_id": str(message.id),
            },
        )
    
    async def _resolve_resume_agent(self, conversation: Conversation) -> BaseAgent:
        if conversation.workflow is None:
            raise ValueError("No active workflow found for conversation.")

        workflow = WorkflowType(conversation.workflow)
        agent_type = self._workflow_agent_mapping[workflow]
        return self._agents[agent_type]

    async def _handle_delegation(
    self,
    conversation_id: UUID,
    delegation: Delegation,
    ) -> None:

        if not delegation:
            raise ValueError("Delegation is required.")

        await self.conversation_service.update_workflow(
            conversation_id=conversation_id,
            workflow=delegation.target.value,
        )

    def _get_delegated_agent(
    self,
    workflow: WorkflowType,
    ) -> BaseAgent:

        if workflow == WorkflowType.ADVISOR:
            return self._get_agent(
                AgentType.ADVISOR,
            )

        if workflow == WorkflowType.INVESTMENT_PURCHASE:
            return self._get_agent(
                AgentType.INVESTMENT,
            )

        raise ValueError(
            f"Unsupported delegation target: {workflow}"
        )
    
    async def _stream_delegated_workflow(
        self,
        conversation: Conversation,
        request: RequestContext,
        delegation: Delegation,
        trace_id: str,
    ) -> AsyncIterator[AgentStreamEvent]:

        target_agent = self._get_delegated_agent(delegation.target)

        history = (await self.conversation_service.get_recent_context(conversation.id))
        delegated_request = replace(
            request,
            query=delegation.payload["query"],
            workflow_resume=None,
            delegation=delegation,
        )

        advisor_state = target_agent.create_state(
            request=delegated_request,
            history=history,
            trace_id=trace_id,
        )

        # ---------------------------------------------------------
        # Start a NEW Advisor stream
        # ---------------------------------------------------------
        async for event in target_agent.stream(advisor_state):
            yield event

    # async def stream(self, request: RequestContext) -> AsyncIterator[AgentStreamEvent]:
    #     trace_id = LangfuseHelper.get_trace_id()

    #     conversation = await self.conversation_service.get_or_create_conversation(
    #                         customer_id=request.customer_id,
    #                         conversation_id=request.conversation_id,
    #                         workflow=None
    #                     )

    #     if request.workflow_resume:
    #         workflow = conversation.workflow
    #         if workflow == WorkflowType.ADVISOR.value:
    #             agent = self._advisor_agent
    #         else:
    #             agent = self._investment_agent
                
    #         await self.conversation_service.add_resume_message(
    #             conversation=conversation,
    #             content=request.workflow_resume,
    #             trace_id=trace_id,
    #         )
    #     else:
    #         await self.conversation_service.add_user_message(
    #             conversation=conversation,
    #             content=request.query,
    #             trace_id=trace_id,
    #         )
        
    #     request.conversation_id = conversation.id
    #     trace_id_ctx.set(trace_id)

    #     result = await self._guardrail_service.validate(request_context=request)

    #     if not result.allowed:
    #         metadata = {
    #             "response_type": "guardrail",
    #             "blocked": True,
    #             "category": result.category.value if result.category else None,
    #             "validator": result.validator,
    #             "reason": result.reason,
    #         }

    #         yield AgentStreamEvent(
    #             type=StreamEventType.COMPLETED.value,
    #             response=LLMStreamResponse(
    #                 answer=result.response,
    #             ),
    #             metadata=metadata,
    #         )

    #         message = await self.conversation_service.add_assistant_message(
    #             conversation=conversation,
    #             content=result.response,
    #             trace_id=trace_id,
    #             metadata=metadata
    #         )

    #         yield AgentStreamEvent(
    #             type=StreamEventType.MESSAGE_SAVED.value,
    #             metadata={
    #                 "message_id": str(message.id),
    #             },
    #         )
    #         return

    #     history = await self.conversation_service.get_recent_context(conversation.id)

    #     agent_request = AgentRequest(
    #         request=request,
    #         conversation=history,
    #     )

    #     plan = await self._agent_router.route(agent_request)

    #     if conversation.workflow != plan.workflow:
    #         await self.conversation_service.update_workflow(
    #             conversation=conversation,
    #             workflow=plan.workflow.value,
    #         )
    #     agent = self._get_agent(plan.primary_agent)
    #     state = agent.create_state(request=request, history=history, trace_id=trace_id)

    #     state.metadata["agent_plan"] = plan.to_dict()

    #     yield AgentStreamEvent(
    #             type=StreamEventType.SESSION.value,
    #             metadata={
    #                 "conversation_id": str(conversation.id),
    #                 "trace_id": str(trace_id)
    #             }
    #         )
    #     stream_response = None 
    #     workflow_interrupt = None

    #     if request.workflow_resume:
    #         stream = agent.resume_stream(state)
    #     else:
    #         stream = agent.stream(state)

    #     async for event in stream:
    #         yield event

    #         if event.type == StreamEventType.COMPLETED.value:
    #             stream_response = event.response

    #         elif event.type == StreamEventType.WORKFLOW_INTERRUPT.value:
    #             workflow_interrupt = event.workflow_interrupt
    #             break

    #     if stream_response:
    #         metadata = {}
    #         metadata["agent_plan"] = state.metadata["agent_plan"]

    #         if stream_response.usage:
    #             metadata['llm_usage'] = asdict(stream_response.usage)
    #         if stream_response.metrics:
    #             metadata['llm_metrics'] = asdict(stream_response.metrics)

    #         message: Message =  await self.conversation_service.add_assistant_message(
    #             conversation=conversation,
    #             content=stream_response.answer,
    #             trace_id=trace_id,
    #             metadata=metadata

    #         )

    #         yield AgentStreamEvent(
    #             type=StreamEventType.MESSAGE_SAVED.value,
    #             metadata={
    #                 "message_id": str(message.id),
    #             },
    #         )
                

    #     elif workflow_interrupt:
    #         await self.conversation_service.add_interrupt_message(
    #             conversation=conversation,
    #             workflow_interrupt=workflow_interrupt,
    #             trace_id=trace_id,
    #         )
            
    def _get_agent(self, agent_type: AgentType) -> BaseAgent:
        try:
            return self._agents[agent_type]
        except KeyError:
            raise ValueError(f"Unsupported agent: {agent_type}")