from langgraph.checkpoint.base import BaseCheckpointSaver
from app.agents.advisor_agent import AdvisorAgent
from app.business.advisor.enums.capabilities import Capability
from app.composition.business.customer_composition import CustomerComposition
from app.composition.business.document_composition import DocumentComposition
from app.composition.business.goal_composition import GoalComposition
from app.composition.business.portfolio_composition import PortfolioComposition
from app.composition.business.scheme_composition import SchemeComposition
from app.composition.llm_composition.gemma_composition import LLMComposition
from app.composition.planner.deterministic_planner_composition import DeterministicPlannerComposition
from app.composition.planner.hybrid_planner_composition import HybridPlannerComposition
from app.composition.prompt.advisor_prompt_composition import AdvisorPromptComposition
from app.composition.tool_composition import ToolComposition
from app.composition.workflow_composition import WorkflowComposition
from app.workflows.advisor.advisor_workflow import AdvisorWorkflow
from app.workflows.advisor.nodes.llm_node import LLMNode
from app.workflows.advisor.nodes.planner_node import PlannerNode
from app.workflows.advisor.nodes.prompt_builder_node import PromptBuilderNode
from app.workflows.advisor.nodes.tool_execution_node import ToolExecutionNode
from app.workflows.advisor.nodes.tool_failure_node import ToolFailureNode
from app.workflows.workflow.node.workflow_node import WorkflowNode


class AdvisorComposition:
    """
    Composition root for the Advisor workflow.

    Responsible only for wiring the application together.
    """

    def __init__(
        self,
        portfolio: PortfolioComposition,
        planner: HybridPlannerComposition,
        scheme: SchemeComposition,
        customer: CustomerComposition,
        goal: GoalComposition,
        document: DocumentComposition,
        tools: ToolComposition,
        prompt: AdvisorPromptComposition,
        llm: LLMComposition,
        workflow: WorkflowComposition,
        checkpointer: BaseCheckpointSaver
    ):
        tools.registry.register(
            definition=portfolio.definition,
            tool=portfolio.tool
        )

        tools.registry.register(
            definition=scheme.definition,
            tool=scheme.tool
        )

        tools.registry.register(
            definition=customer.definition,
            tool=customer.tool
        )

        tools.registry.register(
            definition=goal.definition,
            tool=goal.tool
        )

        tools.registry.register(
            definition=document.definition,
            tool=document.tool
        )
        
        workflow.workflow_service.register(
            Capability.GOAL,
            goal.workflow_handler
        )

        self.planner_node = PlannerNode(
            planner = planner.planner
        )

        self.tool_execution_node = ToolExecutionNode(
            execution_engine=tools.execution_engine
        )

        self.prompt_builder_node = PromptBuilderNode(
            prompt_builder=prompt.prompt_builder
        )

        self.llm_node = LLMNode(
            gateway=llm.gateway
        )

        self.workflow_node = WorkflowNode(workflow.workflow_service)

        self.workflow = AdvisorWorkflow(
            planner_node=self.planner_node,
            tool_exectution_node=self.tool_execution_node,
            tool_failure_node=ToolFailureNode(),
            prompt_builder_node=self.prompt_builder_node,
            llm_node=self.llm_node,
            workflow_node=self.workflow_node,
            checkpointer=checkpointer
        )

        self.agent = AdvisorAgent(
            advisor_workflow=self.workflow
        )