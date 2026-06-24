#                   Version 1
# from fastapi import Depends

# from app.api.dependencies.retrieval import get_context_builder
# from app.api.dependencies.llm import get_llm_gateway
# from app.api.dependencies.tool import get_tool_executor

# from app.retrieval.context_builder import ContextBuilder
# from app.llm_gateway.llm_gateway import LLMGateway
# from app.tools.executor.tool_executor import ToolExecutor

# from app.agents.advisor_agent import AdvisorAgent

# def get_advisor_agent(
#     tool_executor: ToolExecutor = Depends(get_tool_executor),
#     llm_gateway: LLMGateway = Depends(get_llm_gateway),
#     context_builder: ContextBuilder = Depends(get_context_builder)
# ) -> AdvisorAgent:
#     return AdvisorAgent(
#         tool_executor=tool_executor,
#         context_builder=context_builder,
#         llm_gateway=llm_gateway
#     )


from fastapi import Depends

from app.api.dependencies.workflow import get_advisor_workflow
from app.agents.advisor_agent import AdvisorAgent

from app.workflows.advisor.advisor_workflow import AdvisorWorkflow

def get_advisor_agent(
    workflow: AdvisorWorkflow = Depends(get_advisor_workflow)
) -> AdvisorAgent:
    return AdvisorAgent(
        advisor_workflow=workflow
    )