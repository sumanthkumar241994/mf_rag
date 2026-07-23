from pathlib import Path

from app.prompts.enums import PromptType
from app.prompts.evaluator.builder.base_prompt_builder import BasePromptBuilder
from app.prompts.models import Prompt
from app.quality.feedback.enums.insight import IssueCategory, RootCause
from app.quality.feedback.models.feedback_insight_context import (
    FeedbackInsightContext,
)


FEEDBACK_REVIEW_RULES = (
    "Analyze the user's negative feedback together with the conversation.",
    "Identify the primary issue category.",
    "Select exactly ONE root cause from the valid taxonomy.",
    "Do not invent new root causes.",
    "Choose UNKNOWN when none of the root causes apply.",
    "Base the analysis on the user query, assistant response, and user feedback.",
    "Provide a concise engineering-focused summary.",
    "Recommend an actionable fix.",
    "Confidence should reflect how certain you are about the identified root cause.",
)


class FeedbackInsightPromptBuilder(BasePromptBuilder):
    """Builds prompts for Feedback Insight evaluation."""

    TEMPLATE_DIR = Path(__file__).parent.parent / "templates/feedback_insight"
    VERSION = "v1"

    @property
    def type(self) -> PromptType:
        return PromptType.FEEDBACK_INSIGHT

    @property
    def version(self) -> str:
        return self.VERSION

    def build(
        self,
        context: FeedbackInsightContext,
    ) -> Prompt:
        return Prompt(
            type=self.type,
            version=self.version,
            system_prompt=self._load_system_prompt(),
            user_prompt=self._build_user_prompt(context),
        )

    def _load_system_prompt(self) -> str:
        template_path = self.TEMPLATE_DIR / f"feedback_insight_{self.version}.md"
        return template_path.read_text(encoding="utf-8")

    def _build_user_prompt(
        self,
        context: FeedbackInsightContext,
    ) -> str:
        sections = [
            "# Feedback Review Input",
            self._build_conversation_section(context),
            self._build_feedback_section(context),
            self._build_configuration_section(),
        ]

        return "\n\n".join(sections)

    def _build_conversation_section(
        self,
        context: FeedbackInsightContext,
    ) -> str:
        return f"""## User Query

{context.user_message.content}

## Assistant Response

{context.assistant_message.content}
"""

    def _build_feedback_section(
        self,
        context: FeedbackInsightContext,
    ) -> str:
        return f"""## User Feedback

### Signal

{context.feedback.signal.value}

### Reason

{context.feedback.reason.value if context.feedback.reason else "N/A"}

### Comment

{context.feedback.comment or "N/A"}
"""

    def _build_configuration_section(self) -> str:
        return f"""## Feedback Analysis Configuration

### Valid Categories

{self._format_list([category.value for category in IssueCategory])}

### Valid Root Causes

{self._format_list([cause.value for cause in RootCause])}

### Analysis Rules

{self._format_list(FEEDBACK_REVIEW_RULES)}
"""

    @staticmethod
    def _format_list(values: list[str]) -> str:
        if not values:
            return "None"

        return "\n".join(f"- {value}" for value in values)