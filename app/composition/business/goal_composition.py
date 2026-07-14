from app.business.advisor.enums.capabilities import Capability
from app.business.advisor.enums.tool_type import ToolType
from app.business.goal.analyzer.goal_analyzer import GoalAnalyzer
from app.business.goal.calculator.goal_calculator import GoalCalculator
from app.business.goal.context.goal_context_provider import GoalContextProvider
from app.business.goal.parser.goal_parser import GoalParser
from app.business.goal.parser.goal_resume_parser import GoalResumeParser
from app.business.goal.resolver.parameter_resolver import ParameterResolver
from app.business.goal.resolver.retirement_resolver import RetirementResolver
from app.business.goal.service.goal_service import GoalService
from app.composition.workflow_composition import WorkflowComposition
from app.prompts.builder.advisor.sections.goal_section import GoalSection
from app.tools.definitions.tool_definition import ToolDefinition
from app.tools.implementations.goal_tool import GoalTool
from app.workflows.workflow.handlers.goal_workflow_handler import GoalWorkflowHandler
from app.workflows.workflow.service.workflow_service import WorkflowService


class GoalComposition:

    def __init__(
        self,
        workflow_service: WorkflowService,
        goal_context: GoalContextProvider
    ):
        self.goal_parser = GoalParser()
        self.goal_resume_parser = GoalResumeParser()
        self.parameter_resolver = ParameterResolver(retirement_resolver=RetirementResolver())
        self.goal_calculator = GoalCalculator()
        self.goal_analyzer = GoalAnalyzer()

        # Service
        self.goal_service = GoalService(
            parser=self.goal_parser,
            resume_parser=self.goal_resume_parser,
            resolver=self.parameter_resolver,
            calculator=self.goal_calculator,
            analyzer=self.goal_analyzer,
            workflow_service=workflow_service,
            context_provider=goal_context
        )

        # Tool Definition
        self.definition = ToolDefinition(
            name=ToolType.GOAL.value,
            description=(
                "Analyze financial goals such as retirement, "
                "child education, wealth creation and emergency fund "
                "planning. Calculates funding gap, required investment "
                "and provides recommendations."
            ),
            capability=Capability.GOAL,
            timeout_seconds=30,
            tags=[
                "goal",
                "retirement",
                "child-education",
                "wealth-creation",
                "emergency-fund",
                "financial-planning",
            ],
        )

        # Tool
        self.tool = GoalTool(
            goal_service=self.goal_service,
        )

        # Workflow Handler
        self.workflow_handler = GoalWorkflowHandler(
            goal_service=self.goal_service,
        )