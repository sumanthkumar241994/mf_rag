from app.prompts.builder.advisor.advisor_prompt_builder import AdvisorPromptBuilder


class AdvisorPromptComposition:
    def __init__(self) -> None:
        self.prompt_builder = AdvisorPromptBuilder()