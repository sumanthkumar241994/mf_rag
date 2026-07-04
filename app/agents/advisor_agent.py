#                   Version 1
# import time
# from app.dtos.llm.llm_request import LLMRequest

# from app.dtos.llm.llm_response import LLMResponse
# from app.prompts.system.advisor_system_prompt import ADVISOR_SYSTEM_PROMPT
# from app.tools.executor.tool_executor import ToolExecutor
# from app.retrieval.context_builder import ContextBuilder

# from app.llm_gateway.llm_gateway import LLMGateway

# from app.dtos.agents.agent_response import AgentResponse
# from app.schemas.responses.advisor import SourceResponse

# class AdvisorAgent:
#     def __init__(
#         self,
#         tool_executor: ToolExecutor,
#         context_builder: ContextBuilder,
#         llm_gateway: LLMGateway
#     ):
#         self.tool_executor = tool_executor
#         self.context_builder = context_builder
#         self.llm_gateway = llm_gateway
    
#     async def run(self, query: str) -> AgentResponse:
#         start_time = time.perf_counter()
#         # Execute document search tool
#         tool_response = await self.tool_executor.execute(
#             tool_name='document_search',
#             arguments= {
#                 "query": query
#             }
#         )

#         if not tool_response.success:
#             raise RuntimeError(f"Document search failed: {tool_response.error}")
        
#         retrieved_chunks = tool_response.result

#         llm_context = self.context_builder.build(chunks=retrieved_chunks)

#         # Generate answer
#         llm_response = await self.llm_gateway.generate(
#             LLMRequest(
#                 user_prompt=query,
#                 system_prompt=ADVISOR_SYSTEM_PROMPT,
#                 context=llm_context.context
#             )
#         )
#         response_time_ms = round((time.perf_counter()-start_time)*1000)
#         # Return agent response

#         return AgentResponse(
#             answer=llm_response.answer,
#             sources = [
#                 SourceResponse(
#                     source_id=source_id,
#                     scheme_name=chunk.scheme_name,
#                     document_type=chunk.document_type,
#                     section_name=chunk.section_name,
#                     page_no=chunk.page_no
#                 )
#                 for source_id, chunk in llm_context.source_map.items()
#             ],
#             chunk_count=llm_context.chunk_count,
#             response_time_ms=response_time_ms
#         )

# version 2

# from dataclasses import asdict
# import time
# from typing import AsyncIterator

# from app.agents.base_agent import BaseAgent
# from app.dtos.agents.agent_request import AgentRequest
# from app.dtos.request_context import RequestContext
# from app.enums.workflow import WorkflowType
# from app.workflows.advisor.advisor_state import AdvisorState
# from app.workflows.advisor.advisor_workflow import AdvisorWorkflow
# from app.dtos.agents.agent_response import AgentResponse

# class AdvisorAgent(BaseAgent):
#     workflow = WorkflowType.ADVISOR.value

#     def __init__(
#         self,
#         advisor_workflow: AdvisorWorkflow
#     ):
#         self._advisor_workflow = advisor_workflow
    
#     async def run(self, request: AgentRequest) -> AgentResponse:
#         state = AdvisorState(request=request)
#         state = await self._advisor_workflow.invoke(request)

#         metadata = dict(workflow.metadata)

#         if workflow.llm_usage:
#             metadata['llm_usage'] = asdict(workflow.llm_usage)
        
#         if workflow.llm_metrics:
#             metadata['llm_metrics'] =asdict(workflow.llm_metrics)

#         # Return agent response
#         return AgentResponse(
#             answer=state.llm_response.answer if state.llm_res,
#             sources = workflow.sources,
#             chunk_count=workflow.retrieved_chunks,
#             metadata=metadata
#         )
    
#     async def stream(self, request: AgentRequest) -> AsyncIterator[str]:
#         async for event in self.advisor_workflow.stream(request):
#             yield event



from dataclasses import asdict
from typing import AsyncIterator

from app.agents.base_agent import BaseAgent
from app.dtos.agents.stream_event import AgentStreamEvent
from app.enums.workflow import WorkflowType
from app.workflows.advisor.advisor_state import AdvisorState
from app.workflows.advisor.advisor_workflow import AdvisorWorkflow
from app.dtos.agents.agent_response import AgentResponse

class AdvisorAgent(BaseAgent):
    workflow = WorkflowType.ADVISOR.value

    def __init__(
        self,
        advisor_workflow: AdvisorWorkflow
    ):
        self._advisor_workflow = advisor_workflow
    
    async def run(self, state: AdvisorState) -> AgentResponse:
        state = await self._advisor_workflow.invoke(state)

        metadata = state.metadata

        if state.llm_response and state.llm_response.usage is not None:
            metadata['llm_usage'] = asdict(state.llm_response.usage)

        if state.llm_response and state.llm_response.metrics is not None:
            metadata['llm_metrics'] = asdict(state.llm_response.metrics)

        return AgentResponse(
            conversation_id=state.request.conversation_id,
            answer = state.llm_response.answer if state.llm_response else "",
            sources = state.sources,
            chunk_count=state.sources,
            metadata=metadata
        )
    
    async def stream(self, state: AdvisorState) -> AsyncIterator[AgentStreamEvent]:
        async for event in self._advisor_workflow.stream(state):
            yield event