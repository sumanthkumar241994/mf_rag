# app/api/dependencies/workflow.py

from fastapi import Depends

from app.llm_gateway.llm_gateway import LLMGateway
from app.retrieval.context_builder import ContextBuilder
from app.tools.executor.tool_executor import ToolExecutor
from app.workflows.advisor.advisor_workflow import AdvisorWorkflow
from app.workflows.nodes.context.build_context_node import BuildContextNode
from app.workflows.nodes.llm.generate_answer_node import GenerateAnswerNode
from app.workflows.nodes.retrieval.document_search_node import DocumentSearchNode

from app.api.dependencies.tool import get_tool_executor
from app.api.dependencies.retrieval import get_context_builder
from app.api.dependencies.llm import get_llm_gateway

def get_advisor_workflow(
    tool_executor: ToolExecutor = Depends(get_tool_executor),
    context_builder: ContextBuilder = Depends(get_context_builder),
    llm_gateway: LLMGateway = Depends(get_llm_gateway)
    ) -> AdvisorWorkflow:

    document_search_node = DocumentSearchNode(tool_executor=tool_executor)
    build_context_node = BuildContextNode(context_builder=context_builder)
    generate_answer_node = GenerateAnswerNode(llm_gateway=llm_gateway)

    return AdvisorWorkflow(
        document_search_node=document_search_node,
        build_context_node=build_context_node,
        generate_answer_node=generate_answer_node
    )
