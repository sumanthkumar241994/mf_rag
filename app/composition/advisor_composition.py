from redis.asyncio import Redis

from langgraph.checkpoint.base import BaseCheckpointSaver
from sqlalchemy.ext.asyncio import AsyncSession

from app.agents.advisor_agent import AdvisorAgent
from app.business.goal.context.goal_context_provider import GoalContextProvider
from app.business.advisor.enums.capabilities import Capability
from app.compliance.repository.policy_repository import PolicyRepository
from app.compliance.response.streaming.streaming_response_assembler import (
    StreamingResponseAssembler,
)

from app.composition.business.customer_composition import CustomerComposition
from app.composition.business.document_composition import DocumentComposition
from app.composition.business.goal_composition import GoalComposition
from app.composition.business.portfolio_composition import PortfolioComposition
from app.composition.business.scheme_composition import SchemeComposition

from app.composition.database_composition import DatabaseComposition
from app.composition.guardrail_composition import GuardRailComposition
from app.composition.llm_composition.gemma_composition import LLMComposition
from app.composition.planner.hybrid_planner_composition import (
    HybridPlannerComposition,
)
from app.composition.prompt.advisor_prompt_composition import (
    AdvisorPromptComposition,
)
from app.composition.prompt_compliance_composition import (
    PromptComplianceComposition,
)
from app.composition.tool_composition import ToolComposition
from app.composition.workflow_composition import WorkflowComposition

from app.infrastructure.api_client.rest_client import RestApiClient
from app.workflows.advisor.advisor_workflow import AdvisorWorkflow
from app.workflows.advisor.nodes.guardrail_node import GuardRailNode
from app.workflows.advisor.nodes.llm_node import LLMNode
from app.workflows.advisor.nodes.planner_node import PlannerNode
from app.workflows.advisor.nodes.prompt_builder_node import PromptBuilderNode
from app.workflows.advisor.nodes.prompt_compliance_node import (
    PromptComplianceNode,
)
from app.workflows.advisor.nodes.tool_execution_node import ToolExecutionNode
from app.workflows.advisor.nodes.tool_failure_node import ToolFailureNode
from app.workflows.workflow.node.workflow_node import WorkflowNode


class AdvisorComposition:

    def __init__(
        self,
        database: DatabaseComposition,
        redis: Redis,
        rest_api_client: RestApiClient,
        policy_repository: PolicyRepository,
        checkpointer: BaseCheckpointSaver,
        streaming_assembler: StreamingResponseAssembler,
    ):

        #
        # Shared compositions
        #

        workflow = WorkflowComposition()

        llm = LLMComposition()

        planner = HybridPlannerComposition(
            llm.gateway
        )

        tools = ToolComposition()

        prompt = AdvisorPromptComposition()

        prompt_compliance = PromptComplianceComposition(
            policy_repository=policy_repository
        )

        #
        # Business compositions
        #

        portfolio = PortfolioComposition(
            redis=redis,
            rest_api_client=rest_api_client,
            workflow_service=workflow.workflow_service,
        )

        scheme = SchemeComposition(
            rest_api_client=rest_api_client,
            workflow_service=workflow.workflow_service,
        )

        customer = CustomerComposition(
            redis=redis,
            rest_api_client=rest_api_client,
            workflow_service=workflow.workflow_service
        )

        goal_context = GoalContextProvider(
            customer_service=customer.customer_service,
            portfolio_service=portfolio.portofio_service,
        )

        goal = GoalComposition(
            workflow_service=workflow.workflow_service,
            goal_context=goal_context,
        )

        document = DocumentComposition(
            database=database,
            workflow_service=workflow.workflow_service
        )

        #
        # Register tools
        #

        tools.registry.register(
            definition=portfolio.definition,
            tool=portfolio.tool,
        )

        tools.registry.register(
            definition=scheme.definition,
            tool=scheme.tool,
        )

        tools.registry.register(
            definition=customer.definition,
            tool=customer.tool,
        )

        tools.registry.register(
            definition=goal.definition,
            tool=goal.tool,
        )

        tools.registry.register(
            definition=document.definition,
            tool=document.tool,
        )

        #
        # Workflow handlers
        #

        workflow.workflow_service.register(
            Capability.GOAL,
            goal.workflow_handler,
        )

        #
        # Nodes
        #

        planner_node = PlannerNode(
            planner=planner.planner,
        )

        tool_execution_node = ToolExecutionNode(
            execution_engine=tools.execution_engine,
        )

        prompt_builder_node = PromptBuilderNode(
            prompt_builder=prompt.prompt_builder,
        )

        prompt_compliance_node = PromptComplianceNode(
            prompt_compliance.service,
        )

        llm_node = LLMNode(
            gateway=llm.gateway,
        )

        workflow_node = WorkflowNode(
            workflow.workflow_service,
        )

        guardrails = GuardRailComposition(
            llm_gateway=llm.gateway,
        )

        #
        # Workflow
        #

        advisor_workflow = AdvisorWorkflow(
            planner_node=planner_node,
            tool_exectution_node=tool_execution_node,
            tool_failure_node=ToolFailureNode(),
            prompt_builder_node=prompt_builder_node,
            prompt_compliance_node=prompt_compliance_node,
            llm_node=llm_node,
            workflow_node=workflow_node,
            guardrail_node=GuardRailNode(
                guardrail_service=guardrails.guardrail_service,
            ),
            checkpointer=checkpointer,
            response_assembler=streaming_assembler,
        )

        #
        # Agent
        #

        self.agent = AdvisorAgent(
            advisor_workflow=advisor_workflow,
        )