from pathlib import Path

from app.business.advisor.enums.intent import Intent
from app.business.advisor.enums.capabilities import Capability
from app.business.advisor.enums.tool_type import ToolType
from app.prompts.enums import PromptType
from app.prompts.evaluator.builder.base_prompt_builder import BasePromptBuilder
from app.prompts.models import Prompt
from app.quality.evaluation.models.evaluation_context import EvaluationContext

PLANNER_JUDGE_RULES = (
    "Select the single most appropriate intent for the user's primary request.",
    "Select only the capabilities required to satisfy the request.",
    "Avoid selecting unnecessary capabilities.",
    "Ensure selected tools are appropriate for the chosen capabilities.",
    "Multiple capabilities are acceptable when the request spans multiple domains.",
    "Require clarification only when mandatory information is missing or the request is ambiguous.",
)


class PlannerJudgePromptBuilder(BasePromptBuilder):
    """Builds prompts for the Planner Judge."""

    TEMPLATE_DIR = Path(__file__).parent.parent / "templates/planner_judge"
    VERSION = "v1"

    @property
    def type(self) -> PromptType:
        return PromptType.PLANNER_JUDGE

    @property
    def version(self) -> str:
        return self.VERSION

    def build(self, context: EvaluationContext) -> Prompt:
        return Prompt(
            type=self.type,
            version=self.version,
            system_prompt=self._load_system_prompt(),
            user_prompt=self._build_user_prompt(context),
        )

    def _load_system_prompt(self) -> str:
        template_path = self.TEMPLATE_DIR / f"planner_judge_{self.version}.md"
        return template_path.read_text(encoding="utf-8")

    def _build_user_prompt(
        self,
        context: EvaluationContext,
    ) -> str:
        sections = [
            "# Evaluation Input",
            self._build_query_section(context),
            self._build_planner_output_section(context),
            self._build_configuration_section(),
        ]

        return "\n\n".join(sections)

    def _build_query_section(
        self,
        context: EvaluationContext,
    ) -> str:
        return f"""## User Query

{context.user_message.content}
"""

    def _build_planner_output_section(
        self,
        context: EvaluationContext,
    ) -> str:
        planner = context.trace.planner

        return f"""## Planner Output

                ### Intent

                {planner.intent}

                ### Capabilities

                {self._format_list(planner.capabilities)}

                ### Tools

                {self._format_list(planner.selected_tools)}

                ### Confidence

                {planner.confidence:.2f}

                ### Reasoning

                {planner.reasoning or "N/A"}
                """

    def _build_configuration_section(self) -> str:
        return f"""## Planner Configuration

### Valid Intents

{self._format_list([intent.value for intent in Intent])}

### Valid Capabilities

{self._format_list([capability.value for capability in Capability])}

### Valid Tools

{self._format_list([tool.value for tool in ToolType])}

### Planner Rules

{self._format_list(PLANNER_JUDGE_RULES)}
"""

    @staticmethod
    def _format_list(values: list[str]) -> str:
        if not values:
            return "None"

        return "\n".join(f"- {value}" for value in values)