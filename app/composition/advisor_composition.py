from app.agents.advisor_agent import AdvisorAgent
from app.composition.business.portfolio_composition import PortfolioComposition
from app.composition.llm_composition.gemma_composition import LLMComposition
from app.composition.planner.deterministic_planner_composition import DeterministicPlannerComposition
from app.composition.prompt.advisor_prompt_composition import AdvisorPromptComposition
from app.composition.tool_composition import ToolComposition
from app.prompts.advisor.prompt_builder import AdvisorPromptBuilder
from app.workflows.advisor.advisor_workflow import AdvisorWorkflow
from app.workflows.advisor.nodes.llm_node import LLMNode
from app.workflows.advisor.nodes.planner_node import PlannerNode
from app.workflows.advisor.nodes.prompt_builder_node import PromptBuilderNode
from app.workflows.advisor.nodes.tool_execution_node import ToolExecutionNode
from app.workflows.advisor.nodes.tool_failure_node import ToolFailureNode


class AdvisorComposition:
    """
    Composition root for the Advisor workflow.

    Responsible only for wiring the application together.
    """

    def __init__(
        self,
        portfolio: PortfolioComposition,
        planner: DeterministicPlannerComposition,
        tools: ToolComposition,
        prompt: AdvisorPromptComposition,
        llm: LLMComposition
    ):
        tools.registry.register(
            definition=portfolio.definition,
            tool=portfolio.tool
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
            llm_gateway=llm.gateway
        )

        self.workflow = AdvisorWorkflow(
            planner_node=self.planner_node,
            tool_exectution_node=self.tool_execution_node,
            tool_failure_node=ToolFailureNode(),
            prompt_builder_node=self.prompt_builder_node,
            llm_node=self.llm_node
        )

        self.agent = AdvisorAgent(
            advisor_workflow=self.workflow
        )